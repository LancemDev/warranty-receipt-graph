#!/usr/bin/env python3
"""Validate the synthetic warranty report's structure and provenance.

This is a local package-quality check, not a NAS runtime test.
"""
from __future__ import annotations

from datetime import date
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "examples" / "warranty-report.json"

REQUIRED_TOP_LEVEL = {
    "answer",
    "report_meta",
    "warranty_timeline",
    "purchases",
    "findings",
    "evidence",
    "coverage",
    "graph",
    "proposed_next_actions",
    "limitations",
}

STATUSES = {"active", "expiring_soon", "expired", "unknown"}
ROUTE_STATES = {
    "completed",
    "failed",
    "cancelled",
    "waiting_user",
    "waiting_approval",
    "not_run",
}
PROVENANCE_FIELDS = {
    "source_type",
    "agent",
    "cli",
    "action",
    "route_state",
    "source_ref",
}

errors: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    check(set(report) >= REQUIRED_TOP_LEVEL, "missing required top-level section")
    check(report.get("report_meta", {}).get("synthetic_example") is True, "example must be labeled synthetic")

    for section in ("warranty_timeline", "purchases", "findings", "evidence", "coverage", "proposed_next_actions"):
        check(isinstance(report.get(section), list), f"{section} must be a list")

    for item in report["warranty_timeline"]:
        check(item.get("status") in STATUSES, f"invalid warranty status: {item.get('status')}")
        check(bool(item.get("evidence_refs")), "warranty row needs evidence_refs")

    for action in report["proposed_next_actions"]:
        check(action.get("requires_confirmation") is True, "proposed action must require confirmation")
        check(action.get("executed") is False, "proposed action must not be executed")

    for row in report["coverage"]:
        check(row.get("state") in ROUTE_STATES, f"invalid coverage state: {row.get('state')}")

    graph = report["graph"]
    node_ids = set()
    for node in graph["nodes"]:
        check(bool(node.get("id")), "node missing id")
        check(bool(node.get("type")), "node missing type")
        check(isinstance(node.get("props"), dict), "node props must be an object")
        prov = node.get("provenance", {})
        check(PROVENANCE_FIELDS <= set(prov), "node provenance missing fields")
        check(bool(prov.get("source_ref")), "node provenance missing source_ref")
        check(prov.get("route_state") in ROUTE_STATES, "node provenance has invalid route_state")
        node_ids.add(node.get("id"))

    for edge in graph["edges"]:
        check(bool(edge.get("id")), "edge missing id")
        check(bool(edge.get("type")), "edge missing type")
        check(edge.get("from") in node_ids, f"edge from missing node: {edge.get('from')}")
        check(edge.get("to") in node_ids, f"edge to missing node: {edge.get('to')}")
        check(edge.get("status") in {"asserted", "inferred", "ambiguous"}, "edge has invalid status")
        prov = edge.get("provenance", {})
        check(PROVENANCE_FIELDS <= set(prov), "edge provenance missing fields")
        check(bool(prov.get("source_ref")), "edge provenance missing source_ref")
        check(prov.get("route_state") in ROUTE_STATES, "edge provenance has invalid route_state")

    # Verify the expiring-soon example against the declared window.
    meta = report["report_meta"]
    as_of = date.fromisoformat(meta["as_of_date"])
    window = int(meta["expiry_window_days"])
    for item in report["warranty_timeline"]:
        end = item.get("end_date")
        if end:
            end_date = date.fromisoformat(end)
            expected = (
                "expired" if end_date < as_of
                else "expiring_soon" if (end_date - as_of).days <= window
                else "active"
            )
            check(item["status"] == expected, f"warranty status mismatch for {item.get('product')}: expected {expected}")

    # Guard against real NAS paths or obvious secrets in the synthetic example.
    raw = REPORT.read_text(encoding="utf-8")
    check(re.search(r"/nas/|/mnt/|/volume\d*/|/shares/", raw) is None, "example contains a real-looking NAS path")
    check(re.search(r"(?i)(api[_-]?key|password|secret)\s*[:=]\s*['\"]", raw) is None, "example contains a credential-like literal")

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS")
    print(f"nodes={len(graph['nodes'])} edges={len(graph['edges'])} warranties={len(report['warranty_timeline'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
