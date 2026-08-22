#!/usr/bin/env python3
"""Approval-bound provisioning planner for external-knowledge v0.3-beta.1.

This script PLANS only. It never installs, configures, authenticates, repairs,
or executes provider commands.

A plan is eligible for execution by an Agent only after explicit human approval
of the exact plan_id. If any action changes, generate a new plan and obtain new
approval.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


ELIGIBLE_ACTIONS = {"INSTALL_CANDIDATE", "CONFIGURE_CANDIDATE"}
ALLOWED_STEP_KINDS = {
    "run_command",
    "write_config",
    "install_skill",
    "register_mcp",
    "agent_instruction",
}


def load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return data


def canonical_plan_payload(plan: Dict[str, Any]) -> Dict[str, Any]:
    """Fields whose mutation must invalidate prior approval."""
    return {
        "plan_version": plan["plan_version"],
        "runtime": plan.get("runtime"),
        "adapter_id": plan.get("adapter_id"),
        "requested_capabilities": plan.get("requested_capabilities", []),
        "changes": plan.get("changes", []),
        "verification": plan.get("verification", []),
        "unresolved": plan.get("unresolved", []),
    }


def compute_plan_id(plan: Dict[str, Any]) -> str:
    payload = json.dumps(
        canonical_plan_payload(plan),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return "ekp-" + hashlib.sha256(payload).hexdigest()[:20]


def capability_map(doctor: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {
        str(c.get("id")): c
        for c in doctor.get("capabilities", [])
        if isinstance(c, dict) and c.get("id")
    }


def adapter_capability_map(adapter: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {
        str(c.get("id")): c
        for c in adapter.get("capabilities", [])
        if isinstance(c, dict) and c.get("id")
    }


def provider_report_map(cap_report: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {
        str(p.get("id")): p
        for p in cap_report.get("providers", [])
        if isinstance(p, dict) and p.get("id")
    }


def provider_adapter_map(cap_adapter: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {
        str(p.get("id")): p
        for p in cap_adapter.get("providers", [])
        if isinstance(p, dict) and p.get("id")
    }


def parse_provider_selections(values: List[str]) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for raw in values:
        if "=" not in raw:
            raise ValueError(f"--provider must be capability=provider, got: {raw}")
        cap, provider = raw.split("=", 1)
        cap = cap.strip()
        provider = provider.strip()
        if not cap or not provider:
            raise ValueError(f"invalid --provider selection: {raw}")
        out[cap] = provider
    return out


def validate_steps(steps: Any) -> Tuple[bool, str]:
    if not isinstance(steps, list) or not steps:
        return False, "provisioning contract has no concrete steps"
    for i, step in enumerate(steps):
        if not isinstance(step, dict):
            return False, f"step {i} is not an object"
        kind = str(step.get("kind", ""))
        if kind not in ALLOWED_STEP_KINDS:
            return False, f"step {i} has unsupported kind={kind!r}"
        if not step.get("description"):
            return False, f"step {i} lacks description"
        if kind == "run_command":
            argv = step.get("argv")
            if not isinstance(argv, list) or not argv or not all(isinstance(x, str) and x for x in argv):
                return False, f"step {i} run_command requires non-empty argv list"
            if step.get("shell") is True:
                return False, f"step {i} may not request shell=True"
        if kind == "write_config" and not step.get("target"):
            return False, f"step {i} write_config requires target"
        if kind == "register_mcp" and not step.get("target"):
            return False, f"step {i} register_mcp requires target"
        if kind == "install_skill" and not step.get("target"):
            return False, f"step {i} install_skill requires target"
    return True, ""


def provisioning_contract_for(provider: Dict[str, Any], action: str) -> Optional[Dict[str, Any]]:
    prov = provider.get("provisioning")
    if not isinstance(prov, dict):
        return None
    key = "install" if action == "INSTALL_CANDIDATE" else "configure"
    item = prov.get(key)
    return item if isinstance(item, dict) else None


def candidate_providers(cap_report: Dict[str, Any], cap_adapter: Dict[str, Any], action: str) -> List[str]:
    reports = provider_report_map(cap_report)
    adapters = provider_adapter_map(cap_adapter)
    out = []
    for pid, pa in adapters.items():
        pr = reports.get(pid, {})
        contract = provisioning_contract_for(pa, action)
        if not contract:
            continue
        if action == "INSTALL_CANDIDATE" and pr.get("operational_status") != "MISSING_CONFIRMED":
            continue
        if action == "CONFIGURE_CANDIDATE" and pr.get("operational_status") not in {"UNAVAILABLE", "BLOCKED", "UNKNOWN"}:
            continue
        ok, _ = validate_steps(contract.get("steps"))
        if ok:
            out.append(pid)
    return out


def build_change(
    capability_id: str,
    action: str,
    provider_id: str,
    cap_report: Dict[str, Any],
    cap_adapter: Dict[str, Any],
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    reports = provider_report_map(cap_report)
    adapters = provider_adapter_map(cap_adapter)
    pr = reports.get(provider_id)
    pa = adapters.get(provider_id)

    if not pr or not pa:
        return None, f"provider {provider_id!r} not present in both doctor report and adapter"

    contract = provisioning_contract_for(pa, action)
    if not contract:
        return None, f"provider {provider_id!r} has no validated provisioning contract for {action}"

    ok, err = validate_steps(contract.get("steps"))
    if not ok:
        return None, f"invalid provisioning contract for {provider_id!r}: {err}"

    if action == "INSTALL_CANDIDATE" and pr.get("operational_status") != "MISSING_CONFIRMED":
        return None, (
            f"provider {provider_id!r} is {pr.get('operational_status')}; "
            "installation requires provider MISSING_CONFIRMED"
        )

    source = contract.get("source")
    if not source:
        return None, f"provider {provider_id!r} provisioning contract lacks source/provenance"

    change = {
        "capability": capability_id,
        "provider": provider_id,
        "plan_action": action,
        "provider_status_before": pr.get("operational_status"),
        "coverage_grade": pr.get("coverage_grade", "UNKNOWN"),
        "source": source,
        "steps": contract["steps"],
        "failure_policy": (
            "STOP_AND_REPLAN: do not improvise repairs or change commands after approval. "
            "Any changed action requires a new plan_id and new approval."
        ),
    }
    return change, None


def verification_for(change: Dict[str, Any], provider_adapter: Dict[str, Any]) -> List[Dict[str, Any]]:
    prov = provider_adapter.get("provisioning", {})
    key = "install" if change["plan_action"] == "INSTALL_CANDIDATE" else "configure"
    contract = prov.get(key, {}) if isinstance(prov, dict) else {}
    verify = contract.get("verification", [])
    if not isinstance(verify, list) or not verify:
        return [{
            "capability": change["capability"],
            "provider": change["provider"],
            "kind": "doctor_then_representative_probe",
            "success": (
                "Doctor no longer reports the pre-change gap AND, when safe/available, "
                "a representative read-only probe establishes provider availability. "
                "Static presence alone is insufficient."
            ),
        }]
    return [{
        "capability": change["capability"],
        "provider": change["provider"],
        **v,
    } for v in verify if isinstance(v, dict)]


def build_plan(
    doctor: Dict[str, Any],
    adapter: Dict[str, Any],
    requested_capabilities: Optional[List[str]] = None,
    provider_selections: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    provider_selections = provider_selections or {}
    dcaps = capability_map(doctor)
    acaps = adapter_capability_map(adapter)

    if requested_capabilities:
        targets = []
        for cid in requested_capabilities:
            if cid not in targets:
                targets.append(cid)
    else:
        targets = [
            cid for cid, c in dcaps.items()
            if c.get("plan_action") in ELIGIBLE_ACTIONS
        ]

    changes: List[Dict[str, Any]] = []
    verification: List[Dict[str, Any]] = []
    unresolved: List[Dict[str, Any]] = []

    for cid in targets:
        cr = dcaps.get(cid)
        ca = acaps.get(cid)
        if not cr or not ca:
            unresolved.append({"capability": cid, "reason": "missing from doctor report or adapter"})
            continue

        action = str(cr.get("plan_action", ""))
        if action not in ELIGIBLE_ACTIONS:
            unresolved.append({
                "capability": cid,
                "reason": f"capability plan_action={action!r} is not eligible for mutation",
            })
            continue

        candidates = candidate_providers(cr, ca, action)
        selected = provider_selections.get(cid)

        if selected:
            if selected not in candidates:
                unresolved.append({
                    "capability": cid,
                    "reason": f"selected provider {selected!r} is not an eligible validated candidate",
                    "eligible_candidates": candidates,
                })
                continue
        else:
            if len(candidates) == 1:
                selected = candidates[0]
            elif len(candidates) == 0:
                unresolved.append({
                    "capability": cid,
                    "reason": "no provider has a validated provisioning contract matching current provider status",
                })
                continue
            else:
                unresolved.append({
                    "capability": cid,
                    "reason": "multiple eligible providers; explicit provider selection required",
                    "eligible_candidates": candidates,
                })
                continue

        change, err = build_change(cid, action, selected, cr, ca)
        if err:
            unresolved.append({"capability": cid, "provider": selected, "reason": err})
            continue

        changes.append(change)
        pa = provider_adapter_map(ca)[selected]
        verification.extend(verification_for(change, pa))

    plan = {
        "plan_version": 1,
        "planner_version": "0.3-beta",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "runtime": doctor.get("runtime", "unknown"),
        "adapter_id": adapter.get("adapter_id", "unknown"),
        "requested_capabilities": targets,
        "changes": changes,
        "verification": verification,
        "unresolved": unresolved,
        "environment_mutation_attempted": False,
        "approval_required": bool(changes),
        "approval_rule": (
            "Execute only after the user explicitly approves this exact plan_id. "
            "Any change to steps, provider, target, or verification invalidates approval."
        ),
    }
    plan["plan_id"] = compute_plan_id(plan)
    return plan


def render_text(plan: Dict[str, Any]) -> str:
    lines = [
        f"external-knowledge provisioning plan {plan['plan_id']}",
        "=" * 88,
    ]
    if not plan["changes"]:
        lines.append("NO EXECUTABLE CHANGES")
    for change in plan["changes"]:
        lines.append(
            f"{change['capability']} -> {change['provider']} "
            f"[{change['plan_action']}] status_before={change['provider_status_before']}"
        )
        for i, step in enumerate(change["steps"], 1):
            lines.append(f"  {i}. {step['kind']}: {step['description']}")
            if "argv" in step:
                lines.append(f"     argv={json.dumps(step['argv'], ensure_ascii=False)}")
            if "target" in step:
                lines.append(f"     target={step['target']}")
    if plan["unresolved"]:
        lines.append("")
        lines.append("UNRESOLVED:")
        for item in plan["unresolved"]:
            lines.append(f"  - {item}")
    lines.append("")
    lines.append(f"approval_required={plan['approval_required']}")
    lines.append(f"environment_mutation_attempted={plan['environment_mutation_attempted']}")
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(description="Plan external-knowledge provisioning; never execute it")
    p.add_argument("--doctor-report", required=True)
    p.add_argument("--adapter", required=True)
    p.add_argument("--capability", action="append", default=[], help="capability to include; repeatable")
    p.add_argument("--provider", action="append", default=[], help="capability=provider explicit selection; repeatable")
    p.add_argument("--output")
    p.add_argument("--pretty", action="store_true")
    args = p.parse_args()

    try:
        doctor = load_json(args.doctor_report)
        adapter = load_json(args.adapter)
        selections = parse_provider_selections(args.provider)
        plan = build_plan(
            doctor,
            adapter,
            requested_capabilities=(args.capability or None),
            provider_selections=selections,
        )
    except Exception as exc:
        print(f"planner error: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2

    if args.pretty:
        print(render_text(plan))
        print()

    payload = json.dumps(plan, ensure_ascii=False, indent=2)
    print(payload)
    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(payload + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
