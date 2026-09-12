#!/usr/bin/env python3
"""Merge Skill inventory and Doctor output into a read-only machine capability receipt.

Skill claims are attached as carrier/attribution evidence only. Doctor operational
status remains authoritative for capability availability in the supplied runtime scope.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


def load_json(path: str) -> Dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return data


def build_receipt(skill_inventory: Dict[str, Any], doctor_report: Dict[str, Any]) -> Dict[str, Any]:
    claims_by_cap: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    unclassified: List[Dict[str, Any]] = []

    for skill in skill_inventory.get("skills", []):
        if not isinstance(skill, dict):
            continue
        name = str(skill.get("name", ""))
        path = str(skill.get("path", ""))
        claims = skill.get("capability_claims", [])
        if not isinstance(claims, list) or not claims:
            unclassified.append({"name": name, "path": path})
            continue
        for claim in claims:
            if not isinstance(claim, dict):
                continue
            capability = str(claim.get("capability", "")).strip()
            if not capability:
                continue
            claims_by_cap[capability].append({
                "skill": name,
                "path": path,
                "provider": claim.get("provider"),
                "coverage_grade": claim.get("coverage_grade", "UNKNOWN"),
                "claim_status": claim.get("claim_status", "DECLARED_ONLY"),
            })

    capabilities: List[Dict[str, Any]] = []
    doctor_cap_ids = set()
    for cap in doctor_report.get("capabilities", []):
        if not isinstance(cap, dict):
            continue
        cap_id = str(cap.get("id", "")).strip()
        if not cap_id:
            continue
        doctor_cap_ids.add(cap_id)
        capabilities.append({
            "id": cap_id,
            "operational_status": cap.get("operational_status", "UNKNOWN"),
            "best_provider": cap.get("best_provider"),
            "best_available_coverage": cap.get("best_available_coverage", "UNKNOWN"),
            "plan_action": cap.get("plan_action"),
            "skill_carriers": claims_by_cap.get(cap_id, []),
        })

    unmatched_claims = [
        {"capability": cap, "skill_carriers": carriers}
        for cap, carriers in sorted(claims_by_cap.items())
        if cap not in doctor_cap_ids
    ]

    return {
        "receipt_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "runtime": doctor_report.get("runtime", "unknown"),
        "inventory_scope": doctor_report.get("inventory_scope", "not supplied"),
        "skill_roots": skill_inventory.get("roots", []),
        "environment_mutation_attempted": False,
        "capabilities": capabilities,
        "unclassified_skills": unclassified,
        "unmatched_capability_claims": unmatched_claims,
        "interpretation": {
            "operational_status_source": "Doctor report only",
            "skill_carriers_are": "carrier/declared-attribution evidence only",
            "unmatched_claim_means": "declared claim exists but no matching capability was evaluated by the supplied Doctor report",
        },
        "summary": {
            "skill_count": len(skill_inventory.get("skills", [])) if isinstance(skill_inventory.get("skills", []), list) else 0,
            "doctor_capability_count": len(capabilities),
            "capabilities_with_skill_carriers": sum(1 for c in capabilities if c["skill_carriers"]),
            "unclassified_skill_count": len(unclassified),
            "unmatched_claim_count": len(unmatched_claims),
        },
    }


def render_text(receipt: Dict[str, Any]) -> str:
    rows = [
        f"external-knowledge Machine Capability Receipt — runtime={receipt['runtime']}",
        "=" * 100,
    ]
    for cap in receipt["capabilities"]:
        rows.append(
            f"{cap['id']:<24} status={cap['operational_status']:<22} "
            f"best={str(cap.get('best_provider')):<24} coverage={cap.get('best_available_coverage')}"
        )
        for carrier in cap["skill_carriers"]:
            rows.append(
                f"  skill={carrier['skill']} provider_claim={carrier.get('provider')} "
                f"claim_status={carrier.get('claim_status')}"
            )
    if receipt["unclassified_skills"]:
        rows.append("unclassified Skills:")
        for skill in receipt["unclassified_skills"]:
            rows.append(f"  {skill['name']} @ {skill['path']}")
    if receipt["unmatched_capability_claims"]:
        rows.append("unmatched capability claims:")
        for item in receipt["unmatched_capability_claims"]:
            rows.append(f"  {item['capability']}")
    rows.extend([
        "=" * 100,
        "operational status comes only from Doctor; Skill carrier/claims do not upgrade availability",
        "environment_mutation_attempted=False",
    ])
    return "\n".join(rows)


def main(argv: Optional[Iterable[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Merge Skill inventory + Doctor output into a read-only machine capability receipt")
    p.add_argument("--skill-inventory", required=True)
    p.add_argument("--doctor-report", required=True)
    p.add_argument("--output", help="optional JSON receipt path")
    p.add_argument("--pretty", action="store_true")
    args = p.parse_args(list(argv) if argv is not None else None)
    try:
        receipt = build_receipt(load_json(args.skill_inventory), load_json(args.doctor_report))
    except Exception as exc:
        print(f"machine report error: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    if args.pretty:
        print(render_text(receipt))
        print()
    payload = json.dumps(receipt, ensure_ascii=False, indent=2)
    print(payload)
    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(payload + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
