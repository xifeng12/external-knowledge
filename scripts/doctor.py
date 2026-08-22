#!/usr/bin/env python3
"""Read-only capability Doctor for external-knowledge v0.3-beta.1.

alpha.2 normalizes the runtime model:

Capability
  -> Provider binding(s)
     -> independent exposure class(es)
        -> scoped authority/evidence

Registration/container artifacts (for example plugin -> MCP or skill -> CLI)
are evidence carriers, not additional independent exposure classes.

The Doctor never performs network access, installs packages, edits runtime
configuration, or executes provider setup/login commands.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import shutil
import sys
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

VALID_OPERATIONAL = {
    "AVAILABLE",
    "AVAILABLE_WITH_SCOPE",
    "UNKNOWN",
    "UNAVAILABLE",
    "BLOCKED",
    "MISSING_CONFIRMED",
}
VALID_NEEDS = {"REQUIRED", "RECOMMENDED", "WANTED", "OPTIONAL", "NOT_NEEDED"}
VALID_COVERAGE = {"EQUIVALENT", "DEGRADED", "SPECIALIZED", "NOT_APPLICABLE", "UNKNOWN"}


@dataclass
class Evidence:
    source: str
    kind: str
    result: str
    authoritative_for_absence: bool = False
    scope: str = ""
    exposure_class: str = ""
    carrier_class: str = ""
    absence_covers_exposure_classes: List[str] = field(default_factory=list)
    note: str = ""


def _home_redact(value: str) -> str:
    try:
        home = str(Path.home())
        if home and value.startswith(home):
            return "~" + value[len(home):]
    except Exception:
        pass
    return value


def load_json(path: Optional[str]) -> Dict[str, Any]:
    if not path:
        return {}
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return data


def _default_exposure_class(check_type: str) -> str:
    return {
        "command": "path_cli",
        "path": "filesystem_artifact",
        "glob": "filesystem_artifact",
        "env": "environment",
    }.get(check_type, "unclassified")


def local_check(check: Dict[str, Any]) -> Evidence:
    """Execute one deterministic, non-network local observation."""
    typ = str(check.get("type", ""))
    value = str(check.get("value", ""))
    auth = bool(check.get("absence_authoritative", False))
    exposure_class = str(check.get("exposure_class") or _default_exposure_class(typ))
    carrier_class = str(check.get("carrier_class", ""))
    declared_covers = check.get("absence_covers_exposure_classes")
    if isinstance(declared_covers, list):
        covers = [str(x) for x in declared_covers if str(x)]
    else:
        covers = [exposure_class] if auth else []

    try:
        if typ == "command":
            found = shutil.which(value)
            if found:
                return Evidence(
                    source="local_doctor",
                    kind="command_presence",
                    result="PRESENT",
                    scope="current process PATH + executable resolution semantics",
                    exposure_class=exposure_class,
                    carrier_class=carrier_class,
                    note=_home_redact(found),
                )
            return Evidence(
                source="local_doctor",
                kind="command_presence",
                result="ABSENT",
                authoritative_for_absence=auth,
                scope="current process PATH + executable resolution semantics",
                exposure_class=exposure_class,
                carrier_class=carrier_class,
                absence_covers_exposure_classes=covers,
                note=f"command={value}",
            )

        if typ == "path":
            path = Path(os.path.expanduser(value))
            exists = path.exists()
            return Evidence(
                source="local_doctor",
                kind="path_presence",
                result="PRESENT" if exists else "ABSENT",
                authoritative_for_absence=(auth if not exists else False),
                scope="declared filesystem path",
                exposure_class=exposure_class,
                carrier_class=carrier_class,
                absence_covers_exposure_classes=(covers if not exists and auth else []),
                note=_home_redact(str(path)),
            )

        if typ == "glob":
            pattern = os.path.expanduser(value)
            matches = [m for m in glob.glob(pattern) if os.path.exists(m)]
            if matches:
                shown = ", ".join(_home_redact(m) for m in matches[:5])
                if len(matches) > 5:
                    shown += f", ... (+{len(matches)-5})"
                return Evidence(
                    source="local_doctor",
                    kind="glob_presence",
                    result="PRESENT",
                    scope="declared filesystem glob",
                    exposure_class=exposure_class,
                    carrier_class=carrier_class,
                    note=shown,
                )
            return Evidence(
                source="local_doctor",
                kind="glob_presence",
                result="ABSENT",
                authoritative_for_absence=auth,
                scope="declared filesystem glob",
                exposure_class=exposure_class,
                carrier_class=carrier_class,
                absence_covers_exposure_classes=covers,
                note=_home_redact(pattern),
            )

        if typ == "env":
            present = value in os.environ
            return Evidence(
                source="local_doctor",
                kind="env_presence",
                result="PRESENT" if present else "ABSENT",
                authoritative_for_absence=(auth if not present else False),
                scope="current process environment-variable names",
                exposure_class=exposure_class,
                carrier_class=carrier_class,
                absence_covers_exposure_classes=(covers if not present and auth else []),
                note=f"env={value}; value_not_read",
            )

        return Evidence(
            source="local_doctor",
            kind="unsupported_check",
            result="ERROR",
            scope="adapter",
            exposure_class=exposure_class,
            carrier_class=carrier_class,
            note=f"unsupported type={typ!r}",
        )
    except Exception as exc:
        return Evidence(
            source="local_doctor",
            kind=f"{typ or 'unknown'}_check",
            result="ERROR",
            scope="local_check",
            exposure_class=exposure_class,
            carrier_class=carrier_class,
            note=f"{type(exc).__name__}: {exc}",
        )


def inventory_evidence(entry: Dict[str, Any]) -> Evidence:
    status = str(entry.get("status", "UNKNOWN")).upper()
    covers_raw = entry.get("absence_covers_exposure_classes", [])
    covers = [str(x) for x in covers_raw] if isinstance(covers_raw, list) else []
    return Evidence(
        source="agent_inventory",
        kind=str(entry.get("evidence_kind", "agent_inventory")),
        result=status,
        authoritative_for_absence=bool(entry.get("authoritative_for_absence", False)),
        scope=str(entry.get("scope", "current agent runtime")),
        exposure_class=str(entry.get("exposure_class", "runtime_inventory")),
        carrier_class=str(entry.get("carrier_class", "")),
        absence_covers_exposure_classes=covers,
        note=str(entry.get("note", "")),
    )


def exposure_contract(provider: Dict[str, Any]) -> Tuple[Set[str], str]:
    raw = provider.get("exposure_contract")
    if not isinstance(raw, dict):
        return set(), ""
    classes = raw.get("legal_classes", [])
    legal = {str(x) for x in classes if str(x)} if isinstance(classes, list) else set()
    return legal, str(raw.get("scope", ""))


def _authoritative_absent_classes(evidence: List[Evidence]) -> Set[str]:
    covered: Set[str] = set()
    for e in evidence:
        if not e.authoritative_for_absence:
            continue
        if e.result not in {"ABSENT", "MISSING_CONFIRMED", "UNKNOWN"}:
            continue
        covered.update(x for x in e.absence_covers_exposure_classes if x)
    return covered


def merge_provider_status(
    provider: Dict[str, Any],
    local: List[Evidence],
    inventory_entry: Optional[Dict[str, Any]],
) -> Tuple[str, List[str], Dict[str, Any]]:
    """Merge evidence for one provider binding."""
    reasons: List[str] = []
    legal_classes, contract_scope = exposure_contract(provider)
    ev = list(local)
    if inventory_entry:
        ev.append(inventory_evidence(inventory_entry))

    requested = "UNKNOWN"
    if inventory_entry:
        requested = str(inventory_entry.get("status", "UNKNOWN")).upper()
        if requested not in VALID_OPERATIONAL:
            reasons.append(f"invalid inventory status {requested!r}; downgraded to UNKNOWN")
            requested = "UNKNOWN"

        kind = str(inventory_entry.get("evidence_kind", "agent_inventory"))
        if requested in {"AVAILABLE", "AVAILABLE_WITH_SCOPE", "UNAVAILABLE", "BLOCKED"}:
            reasons.append(f"runtime evidence ({kind}) establishes provider {requested} for its stated scope")
            detail = {
                "legal_exposure_classes": sorted(legal_classes),
                "contract_scope": contract_scope,
                "authoritative_absent_classes": sorted(_authoritative_absent_classes(ev)),
                "uncovered_legal_classes": [],
                "conflicting_present_classes": [],
                "ignored_present_classes": [],
                "carrier_classes_observed": sorted({e.carrier_class for e in ev if e.carrier_class}),
            }
            return requested, reasons, detail

        if requested == "MISSING_CONFIRMED" and not bool(inventory_entry.get("authoritative_for_absence", False)):
            reasons.append("inventory claimed MISSING_CONFIRMED without authoritative absence; treated as UNKNOWN")
            requested = "UNKNOWN"

    present_legal = sorted({
        e.exposure_class for e in ev
        if e.result == "PRESENT" and e.exposure_class in legal_classes
    })
    present_outside = sorted({
        e.exposure_class for e in ev
        if e.result == "PRESENT" and e.exposure_class and e.exposure_class not in legal_classes
    })
    auth_absent = _authoritative_absent_classes(ev)
    uncovered = sorted(legal_classes - auth_absent)
    carrier_classes = sorted({e.carrier_class for e in ev if e.carrier_class})

    detail = {
        "legal_exposure_classes": sorted(legal_classes),
        "contract_scope": contract_scope,
        "authoritative_absent_classes": sorted(auth_absent),
        "uncovered_legal_classes": uncovered,
        "conflicting_present_classes": present_legal,
        "ignored_present_classes": present_outside,
        "carrier_classes_observed": carrier_classes,
    }

    if carrier_classes:
        reasons.append(
            "carrier/registration evidence observed but not counted as independent exposure classes: "
            + ", ".join(carrier_classes)
        )

    if not legal_classes:
        reasons.append("provider has no declared independent exposure-class contract; missing cannot be confirmed")
    else:
        if present_legal:
            reasons.append("PRESENT evidence exists inside legal exposure classes: " + ", ".join(present_legal))
        if present_outside:
            reasons.append(
                "PRESENT evidence outside legal exposure classes does not block provider missing confirmation: "
                + ", ".join(present_outside)
            )
        if uncovered:
            reasons.append(
                "authoritative absence does not cover all legal exposure classes; uncovered="
                + ", ".join(uncovered)
            )
        if not present_legal and not uncovered:
            reasons.append(
                "all provider legal exposure classes are authoritatively absent with no in-contract PRESENT conflict"
            )
            return "MISSING_CONFIRMED", reasons, detail

    if requested == "MISSING_CONFIRMED":
        reasons.append("provider-level MISSING_CONFIRMED claim was not justified by exposure coverage; downgraded to UNKNOWN")
    elif inventory_entry:
        reasons.append("provider runtime evidence remains UNKNOWN")

    if any(e.result == "PRESENT" for e in local) and not present_legal:
        reasons.append("static/local presence outside legal execution surfaces does not prove provider callability")
    if any(e.result == "ERROR" for e in local):
        reasons.append("one or more local checks errored; Doctor continued")

    return "UNKNOWN", reasons, detail


def _coverage_rank(grade: str) -> int:
    return {
        "EQUIVALENT": 4,
        "SPECIALIZED": 3,
        "DEGRADED": 2,
        "UNKNOWN": 1,
        "NOT_APPLICABLE": 0,
    }.get(grade, 1)


def aggregate_capability(providers: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Aggregate provider states without equating one provider with a capability."""
    available = [
        p for p in providers
        if p["operational_status"] in {"AVAILABLE", "AVAILABLE_WITH_SCOPE"}
    ]
    if available:
        best = max(available, key=lambda p: _coverage_rank(p.get("coverage_grade", "UNKNOWN")))
        best_grade = best.get("coverage_grade", "UNKNOWN")
        status = "AVAILABLE" if best_grade == "EQUIVALENT" else "AVAILABLE_WITH_SCOPE"
        return {
            "operational_status": status,
            "best_provider": best["id"],
            "best_available_coverage": best_grade,
            "reason": "at least one provider is operational; provider missing does not imply capability missing",
        }

    if providers and all(p["operational_status"] == "MISSING_CONFIRMED" for p in providers):
        return {
            "operational_status": "MISSING_CONFIRMED",
            "best_provider": None,
            "best_available_coverage": "NOT_APPLICABLE",
            "reason": "all declared provider bindings are MISSING_CONFIRMED",
        }

    if providers and all(p["operational_status"] in {"UNAVAILABLE", "BLOCKED", "MISSING_CONFIRMED"} for p in providers):
        return {
            "operational_status": "UNAVAILABLE",
            "best_provider": None,
            "best_available_coverage": "NOT_APPLICABLE",
            "reason": "no provider is operational and none remains UNKNOWN",
        }

    return {
        "operational_status": "UNKNOWN",
        "best_provider": None,
        "best_available_coverage": "UNKNOWN",
        "reason": "no provider is operational and at least one provider remains UNKNOWN",
    }


def parse_need_entry(raw: Any) -> Tuple[Optional[str], str, str]:
    if raw is None:
        return None, "UNKNOWN", ""
    if isinstance(raw, str):
        return raw.upper(), "UNKNOWN", ""
    if isinstance(raw, dict):
        need = str(raw.get("level", raw.get("need", ""))).upper() or None
        fallback = str(raw.get("equivalent_fallback", "UNKNOWN")).upper()
        if fallback not in {"YES", "NO", "UNKNOWN"}:
            fallback = "UNKNOWN"
        return need, fallback, str(raw.get("note", ""))
    return None, "UNKNOWN", "invalid need entry"


def plan_capability_action(
    capability_status: str,
    need: Optional[str],
    best_coverage: str,
    equivalent_fallback: str = "UNKNOWN",
) -> Optional[str]:
    if need is None:
        return None
    need = need.upper()
    if need not in VALID_NEEDS:
        return "UNRESOLVED"

    if need in {"OPTIONAL", "NOT_NEEDED"}:
        return "DO_NOT_INSTALL"

    if capability_status == "AVAILABLE":
        return "KEEP"

    if capability_status == "AVAILABLE_WITH_SCOPE":
        # Alpha does not auto-install challengers merely because coverage is degraded/specialized.
        return "KEEP"

    if capability_status == "MISSING_CONFIRMED":
        if equivalent_fallback == "YES":
            return "DO_NOT_INSTALL"
        if equivalent_fallback == "NO":
            return "INSTALL_CANDIDATE"
        return "UNRESOLVED"

    if capability_status in {"UNKNOWN", "UNAVAILABLE", "BLOCKED"}:
        return "TARGETED_DIAGNOSIS"

    return "UNRESOLVED"


def _provider_inventory_entry(agent_caps: Dict[str, Any], capability_id: str, provider: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    cap_entry = agent_caps.get(capability_id)
    if not isinstance(cap_entry, dict):
        return None

    providers = cap_entry.get("providers")
    if isinstance(providers, dict):
        entry = providers.get(provider["id"])
        return entry if isinstance(entry, dict) else None

    # Compatibility path for a single-provider/old inventory: only use it when
    # provider explicitly declares that key.
    legacy_key = provider.get("legacy_inventory_key")
    if legacy_key and legacy_key == capability_id:
        return cap_entry

    return None


def diagnose(adapter: Dict[str, Any], agent: Dict[str, Any], needs: Dict[str, Any]) -> Dict[str, Any]:
    agent_caps = agent.get("capabilities", {}) if isinstance(agent.get("capabilities", {}), dict) else {}
    need_map = needs.get("needs", {}) if isinstance(needs.get("needs", {}), dict) else {}

    capabilities = []
    provider_status_counts: Dict[str, int] = {}

    for cap in adapter.get("capabilities", []):
        cap_id = str(cap.get("id", "")).strip()
        if not cap_id:
            continue

        provider_reports = []
        for provider in cap.get("providers", []):
            if not isinstance(provider, dict):
                continue
            provider_id = str(provider.get("id", "")).strip()
            if not provider_id:
                continue

            local = [local_check(c) for c in provider.get("checks", []) if isinstance(c, dict)]
            entry = _provider_inventory_entry(agent_caps, cap_id, provider)
            ev = list(local)
            if entry:
                ev.append(inventory_evidence(entry))

            status, reasons, merge_detail = merge_provider_status(provider, local, entry)
            coverage = str(provider.get("coverage_grade", "UNKNOWN")).upper()
            if coverage not in VALID_COVERAGE:
                coverage = "UNKNOWN"

            provider_status_counts[status] = provider_status_counts.get(status, 0) + 1
            provider_reports.append({
                "id": provider_id,
                "label": provider.get("label", provider_id),
                "operational_status": status,
                "coverage_grade": coverage,
                "exposure_merge": merge_detail,
                "reasons": reasons,
                "evidence": [asdict(x) for x in ev],
            })

        aggregate = aggregate_capability(provider_reports)
        need, equivalent_fallback, need_note = parse_need_entry(need_map.get(cap_id))
        action = plan_capability_action(
            aggregate["operational_status"],
            need,
            aggregate["best_available_coverage"],
            equivalent_fallback,
        )

        capabilities.append({
            "id": cap_id,
            "operational_status": aggregate["operational_status"],
            "best_provider": aggregate["best_provider"],
            "best_available_coverage": aggregate["best_available_coverage"],
            "aggregate_reason": aggregate["reason"],
            "need": need,
            "equivalent_fallback": equivalent_fallback,
            "need_note": need_note,
            "plan_action": action,
            "providers": provider_reports,
        })

    cap_counts: Dict[str, int] = {}
    for item in capabilities:
        cap_counts[item["operational_status"]] = cap_counts.get(item["operational_status"], 0) + 1

    return {
        "report_version": 3,
        "doctor_version": "0.3-alpha.2",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "adapter_id": adapter.get("adapter_id", "unknown"),
        "runtime": agent.get("runtime", "unknown") if agent else "unknown",
        "inventory_scope": agent.get("inventory_scope", "not supplied") if agent else "not supplied",
        "environment_mutation_attempted": False,
        "capabilities": capabilities,
        "summary": {
            "capability_status_counts": cap_counts,
            "provider_status_counts": provider_status_counts,
            "capability_count": len(capabilities),
            "provider_count": sum(len(c["providers"]) for c in capabilities),
        },
    }


def render_text(report: Dict[str, Any]) -> str:
    rows = [
        f"external-knowledge Doctor {report.get('doctor_version','')} — "
        f"adapter={report['adapter_id']} runtime={report['runtime']}",
        "=" * 108,
    ]
    for c in report["capabilities"]:
        need = c.get("need") or "-"
        rows.append(
            f"{c['id']:<24} {c['operational_status']:<22} "
            f"need={need:<12} best={str(c.get('best_provider')):<24} "
            f"coverage={c.get('best_available_coverage'):<12} action={c.get('plan_action')}"
        )
        rows.append(f"  aggregate: {c.get('aggregate_reason')}")
        for p in c.get("providers", []):
            rows.append(
                f"  provider {p['id']:<22} status={p['operational_status']:<20} "
                f"coverage={p['coverage_grade']}"
            )
            m = p.get("exposure_merge", {})
            if m.get("legal_exposure_classes"):
                rows.append(
                    "    exposure: legal="
                    + ",".join(m["legal_exposure_classes"])
                    + " absent="
                    + ",".join(m.get("authoritative_absent_classes", []))
                    + " conflict="
                    + ",".join(m.get("conflicting_present_classes", []))
                )
            if m.get("carrier_classes_observed"):
                rows.append("    carriers=" + ",".join(m["carrier_classes_observed"]))
            for reason in p.get("reasons", []):
                rows.append(f"    reason: {reason}")
    rows.extend([
        "=" * 108,
        f"environment_mutation_attempted={report['environment_mutation_attempted']}",
    ])
    return "\n".join(rows)


def main(argv: Optional[Iterable[str]] = None) -> int:
    p = argparse.ArgumentParser(
        description="Read-only capability/provider Doctor for external-knowledge v0.3-beta.1"
    )
    p.add_argument("--adapter", required=True, help="runtime adapter JSON")
    p.add_argument("--agent-inventory", help="Agent runtime inventory JSON")
    p.add_argument("--needs", help="Need profile JSON")
    p.add_argument("--output", help="optional JSON report path")
    p.add_argument("--pretty", action="store_true", help="print human-readable report before JSON")
    args = p.parse_args(list(argv) if argv is not None else None)

    try:
        adapter = load_json(args.adapter)
        agent = load_json(args.agent_inventory)
        needs = load_json(args.needs)
        report = diagnose(adapter, agent, needs)
    except Exception as exc:
        print(f"doctor error: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2

    if args.pretty:
        print(render_text(report))
        print()

    payload = json.dumps(report, ensure_ascii=False, indent=2)
    print(payload)

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(payload + "\n", encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
