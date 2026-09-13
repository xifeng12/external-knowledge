#!/usr/bin/env python3
"""Generate a deterministic, non-evidentiary Agent runtime inventory scaffold.

The scaffold is derived only from a runtime adapter. It performs no runtime,
filesystem, environment, network, provider, credential, or registration probes.
Every provider begins UNKNOWN and non-authoritative for absence.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

INVENTORY_VERSION = 4


def load_adapter(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"adapter JSON root must be an object: {path}")
    return data


def _legal_classes(provider: Dict[str, Any]) -> list[str]:
    raw = provider.get("exposure_contract")
    if not isinstance(raw, dict):
        return []
    classes = raw.get("legal_classes", [])
    if not isinstance(classes, list):
        return []
    return sorted({str(x) for x in classes if str(x)})


def build_scaffold(adapter: Dict[str, Any]) -> Dict[str, Any]:
    capabilities: Dict[str, Any] = {}

    for capability in adapter.get("capabilities", []):
        if not isinstance(capability, dict):
            continue
        capability_id = str(capability.get("id", "")).strip()
        if not capability_id:
            continue

        providers: Dict[str, Any] = {}
        for provider in capability.get("providers", []):
            if not isinstance(provider, dict):
                continue
            provider_id = str(provider.get("id", "")).strip()
            if not provider_id:
                continue

            providers[provider_id] = {
                "status": "UNKNOWN",
                "evidence_kind": "UNSET",
                "scope": "",
                "authoritative_for_absence": False,
                "exposure_class": "",
                "carrier_class": "",
                "absence_covers_exposure_classes": [],
                "declared_legal_exposure_classes": _legal_classes(provider),
                "note": "",
            }

        if providers:
            capabilities[capability_id] = {"providers": providers}

    return {
        "inventory_version": INVENTORY_VERSION,
        "runtime": "unknown",
        "inventory_scope": "scaffold only; replace with the actual observed Agent/runtime scope",
        "capabilities": capabilities,
    }


def render(scaffold: Dict[str, Any], pretty: bool) -> str:
    if pretty:
        return json.dumps(scaffold, ensure_ascii=False, indent=2)
    return json.dumps(scaffold, ensure_ascii=False, separators=(",", ":"))


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate a read-only Agent runtime inventory scaffold from one adapter JSON"
    )
    parser.add_argument("--adapter", required=True, help="runtime adapter JSON path")
    parser.add_argument("--output", help="optional output JSON path")
    parser.add_argument("--pretty", action="store_true", help="pretty-print JSON")
    args = parser.parse_args(list(argv) if argv is not None else None)

    try:
        scaffold = build_scaffold(load_adapter(args.adapter))
        payload = render(scaffold, args.pretty)
    except Exception as exc:
        print(f"inventory scaffold error: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2

    print(payload)

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(payload + "\n", encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
