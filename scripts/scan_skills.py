#!/usr/bin/env python3
"""Read-only Skill inventory scanner for external-knowledge diagnostics.

This scanner answers a narrow question: which Skill packages are discoverable under
explicitly supplied roots, and which external-knowledge capabilities do those Skill
packages explicitly *claim* to contribute?

It does not execute Skills, call network services, inspect secret values, install or
configure anything, or infer operational capability from Skill presence.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

SCHEMA_VERSION = 1
SIDECAR_NAME = "external-knowledge.json"


def _home_redact(value: str) -> str:
    try:
        home = str(Path.home())
        if home and value.startswith(home):
            return "~" + value[len(home):]
    except Exception:
        pass
    return value


def _read_frontmatter(path: Path) -> Dict[str, str]:
    """Read only simple top-level scalar frontmatter fields used for inventory.

    The scanner intentionally does not implement general YAML. It extracts `name` and
    a one-line `description` when present. Complex/multiline YAML remains unparsed
    rather than guessed.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return {}
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    result: Dict[str, str] = {}
    for raw in lines[1:]:
        if raw.strip() == "---":
            break
        if not raw or raw[0].isspace() or ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key in {"name", "description"} and value and value not in {"|", ">"}:
            result[key] = value
    return result


def _load_sidecar(skill_dir: Path) -> Dict[str, Any]:
    path = skill_dir / SIDECAR_NAME
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {
            "_error": f"{type(exc).__name__}: {exc}",
            "_path": _home_redact(str(path)),
        }
    if not isinstance(data, dict):
        return {
            "_error": "sidecar root must be a JSON object",
            "_path": _home_redact(str(path)),
        }
    data["_path"] = _home_redact(str(path))
    return data


def _normalize_claims(sidecar: Dict[str, Any]) -> List[Dict[str, Any]]:
    raw = sidecar.get("capability_claims", [])
    if not isinstance(raw, list):
        return []
    claims: List[Dict[str, Any]] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        capability = str(item.get("capability", "")).strip()
        if not capability:
            continue
        provider = str(item.get("provider", "")).strip() or None
        coverage = str(item.get("coverage_grade", "UNKNOWN")).upper()
        claims.append({
            "capability": capability,
            "provider": provider,
            "coverage_grade": coverage,
            "claim_status": "DECLARED_ONLY",
            "note": str(item.get("note", "")),
        })
    return claims


def discover_skill_dirs(root: Path) -> List[Path]:
    """Return directories containing SKILL.md beneath one explicit root."""
    if not root.exists() or not root.is_dir():
        return []
    found: List[Path] = []
    try:
        for skill_md in root.rglob("SKILL.md"):
            if skill_md.is_file():
                found.append(skill_md.parent)
    except Exception:
        return found
    return sorted(set(found), key=lambda p: str(p).lower())


def scan_roots(roots: Iterable[str]) -> Dict[str, Any]:
    normalized_roots: List[Path] = []
    root_reports: List[Dict[str, Any]] = []
    for raw in roots:
        p = Path(os.path.expandvars(os.path.expanduser(raw))).resolve()
        normalized_roots.append(p)
        root_reports.append({
            "path": _home_redact(str(p)),
            "exists": p.exists(),
            "is_dir": p.is_dir(),
        })

    seen: set[str] = set()
    skills: List[Dict[str, Any]] = []
    for root in normalized_roots:
        for skill_dir in discover_skill_dirs(root):
            canonical = str(skill_dir.resolve())
            if canonical in seen:
                continue
            seen.add(canonical)
            skill_md = skill_dir / "SKILL.md"
            frontmatter = _read_frontmatter(skill_md)
            sidecar = _load_sidecar(skill_dir)
            claims = _normalize_claims(sidecar)
            sidecar_error = str(sidecar.get("_error", "")) if sidecar else ""
            skills.append({
                "name": frontmatter.get("name") or skill_dir.name,
                "description": frontmatter.get("description", ""),
                "path": _home_redact(canonical),
                "carrier_status": "DISCOVERED",
                "capability_claims": claims,
                "capability_attribution": "EXPLICIT_DECLARATION" if claims else "UNCLASSIFIED",
                "sidecar": {
                    "present": bool(sidecar),
                    "path": sidecar.get("_path", "") if sidecar else "",
                    "error": sidecar_error,
                },
            })

    skills.sort(key=lambda x: (str(x["name"]).lower(), str(x["path"]).lower()))
    claim_count = sum(len(s["capability_claims"]) for s in skills)
    classified = sum(1 for s in skills if s["capability_claims"])
    return {
        "report_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "environment_mutation_attempted": False,
        "roots": root_reports,
        "skills": skills,
        "summary": {
            "skill_count": len(skills),
            "classified_skill_count": classified,
            "unclassified_skill_count": len(skills) - classified,
            "declared_capability_claim_count": claim_count,
        },
        "interpretation": {
            "skill_presence_proves": "carrier/discovery presence only",
            "declared_capability_claim_proves": "a Skill package claims a capability mapping",
            "does_not_prove": "provider or capability operational availability",
            "next_evidence": "runtime exposure or representative probe, merged by Doctor",
        },
    }


def render_text(report: Dict[str, Any]) -> str:
    rows = [
        "external-knowledge Skill Inventory",
        "=" * 88,
    ]
    for skill in report["skills"]:
        rows.append(
            f"{skill['name']:<28} carrier={skill['carrier_status']:<10} "
            f"attribution={skill['capability_attribution']}"
        )
        rows.append(f"  path={skill['path']}")
        for claim in skill["capability_claims"]:
            rows.append(
                f"  claim capability={claim['capability']} provider={claim.get('provider')} "
                f"coverage={claim['coverage_grade']} status={claim['claim_status']}"
            )
    rows.extend([
        "=" * 88,
        f"skills={report['summary']['skill_count']} "
        f"classified={report['summary']['classified_skill_count']} "
        f"claims={report['summary']['declared_capability_claim_count']}",
        "presence/claim != operational availability",
        "environment_mutation_attempted=False",
    ])
    return "\n".join(rows)


def main(argv: Optional[Iterable[str]] = None) -> int:
    p = argparse.ArgumentParser(
        description="Read-only inventory of installed/discoverable Skill packages and explicit external-knowledge capability claims"
    )
    p.add_argument(
        "--root",
        action="append",
        required=True,
        help="Skill root to scan; repeat for multiple roots. Roots are explicit to avoid pretending one registry view is machine-wide.",
    )
    p.add_argument("--output", help="optional JSON report path")
    p.add_argument("--pretty", action="store_true", help="print human-readable report before JSON")
    args = p.parse_args(list(argv) if argv is not None else None)

    try:
        report = scan_roots(args.root)
    except Exception as exc:
        print(f"skill inventory error: {type(exc).__name__}: {exc}", file=sys.stderr)
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
