#!/usr/bin/env python3
"""Validate a machine-readable change split plan."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict, deque
from pathlib import Path
from typing import Any


KINDS = {
    "structure",
    "behavior",
    "data",
    "docs",
    "test",
    "operations",
    "cleanup",
    "expand",
    "contract",
}
STRATEGIES = {
    "direct",
    "flag",
    "expand",
    "contract",
    "strangler",
    "branch-by-abstraction",
    "not-applicable",
}
CONJUNCTION = re.compile(
    r"\b(and|plus|as well as)\b|(?:および|及び|かつ|ならびに|並びに)",
    re.IGNORECASE,
)


def is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def add(diags: list[dict[str, str]], severity: str, path: str, message: str) -> None:
    diags.append({"severity": severity, "path": path, "message": message})


def validate_independence(
    unit: dict[str, Any], index: int, diags: list[dict[str, str]]
) -> None:
    base = f"units[{index}].independence"
    independence = unit.get("independence")
    if not isinstance(independence, dict):
        add(diags, "error", base, "must be an object with build, test, and deploy")
        return
    for stage in ("build", "test", "deploy"):
        item = independence.get(stage)
        path = f"{base}.{stage}"
        if not isinstance(item, dict):
            add(diags, "error", path, "must be an object")
            continue
        if not isinstance(item.get("possible"), bool):
            add(diags, "error", f"{path}.possible", "must be boolean")
        evidence = item.get("evidence")
        if not is_nonempty_string(evidence):
            add(diags, "warning", f"{path}.evidence", "add concrete verification evidence")
        if item.get("possible") is False:
            add(
                diags,
                "warning",
                f"{path}.possible",
                "unit is not independently verifiable; add a transition strategy or split again",
            )


def validate_unit(
    unit: Any, index: int, threshold: float, diags: list[dict[str, str]]
) -> str | None:
    base = f"units[{index}]"
    if not isinstance(unit, dict):
        add(diags, "error", base, "must be an object")
        return None

    unit_id = unit.get("id")
    if not is_nonempty_string(unit_id):
        add(diags, "error", f"{base}.id", "must be a non-empty string")
        unit_id = None

    for field in ("intent", "value", "rollback"):
        if not is_nonempty_string(unit.get(field)):
            add(diags, "error", f"{base}.{field}", "must be a non-empty string")

    intent = unit.get("intent")
    if is_nonempty_string(intent):
        sentence_marks = len(re.findall(r"[.!?。！？]", intent.strip().rstrip(".!?。！？")))
        if sentence_marks:
            add(diags, "warning", f"{base}.intent", "appears to contain multiple sentences")
        if CONJUNCTION.search(intent):
            add(
                diags,
                "warning",
                f"{base}.intent",
                "contains a conjunction; review for multiple logical concerns",
            )

    cost = unit.get("estimated_cost")
    if not (
        (isinstance(cost, (int, float)) and not isinstance(cost, bool) and cost >= 0)
        or is_nonempty_string(cost)
    ):
        add(
            diags,
            "error",
            f"{base}.estimated_cost",
            "must be a non-negative number or non-empty qualitative estimate",
        )

    dependencies = unit.get("depends_on")
    if not isinstance(dependencies, list) or not all(
        is_nonempty_string(item) for item in dependencies
    ):
        add(diags, "error", f"{base}.depends_on", "must be an array of unit IDs")

    change = unit.get("change")
    if not isinstance(change, dict):
        add(diags, "error", f"{base}.change", "must be an object")
    else:
        kind = change.get("kind")
        if kind == "mixed":
            add(
                diags,
                "error",
                f"{base}.change.kind",
                "split structural and behavioral concerns into separate units",
            )
        elif kind not in KINDS:
            add(
                diags,
                "error",
                f"{base}.change.kind",
                f"must be one of: {', '.join(sorted(KINDS))}",
            )
        targets = change.get("targets")
        if not isinstance(targets, list) or not targets or not all(
            is_nonempty_string(item) for item in targets
        ):
            add(
                diags,
                "error",
                f"{base}.change.targets",
                "must be a non-empty array of affected targets",
            )
        if not isinstance(change.get("single_cluster"), bool):
            add(
                diags,
                "error",
                f"{base}.change.single_cluster",
                "must be boolean",
            )
        elif change.get("single_cluster") is False:
            add(
                diags,
                "error",
                f"{base}.change.single_cluster",
                "multiple dependency clusters require another split or explicit justification",
            )

    validate_independence(unit, index, diags)

    strategy = unit.get("delivery_strategy")
    if strategy not in STRATEGIES:
        add(
            diags,
            "error",
            f"{base}.delivery_strategy",
            f"must be one of: {', '.join(sorted(STRATEGIES))}",
        )
    if strategy == "contract" and not is_nonempty_string(unit.get("contract_for")):
        add(
            diags,
            "error",
            f"{base}.contract_for",
            "contract units must identify the unit they clean up",
        )

    lines = unit.get("estimated_lines")
    if not (
        isinstance(lines, (int, float)) and not isinstance(lines, bool) and lines >= 0
    ):
        add(diags, "error", f"{base}.estimated_lines", "must be a non-negative number")
    elif lines > threshold:
        add(
            diags,
            "warning",
            f"{base}.estimated_lines",
            f"{lines:g} exceeds the {threshold:g}-line warning threshold; inspect cohesion",
        )

    return unit_id


def validate_graph(
    units: list[Any], ids: list[str | None], order: Any, diags: list[dict[str, str]]
) -> None:
    clean_ids = [unit_id for unit_id in ids if unit_id is not None]
    id_set = set(clean_ids)
    if len(id_set) != len(clean_ids):
        seen: set[str] = set()
        for index, unit_id in enumerate(ids):
            if unit_id is not None and unit_id in seen:
                add(diags, "error", f"units[{index}].id", f"duplicate ID: {unit_id}")
            elif unit_id is not None:
                seen.add(unit_id)

    graph: dict[str, list[str]] = defaultdict(list)
    indegree = {unit_id: 0 for unit_id in id_set}
    for index, unit in enumerate(units):
        if not isinstance(unit, dict) or ids[index] is None:
            continue
        unit_id = ids[index]
        dependencies = unit.get("depends_on")
        if not isinstance(dependencies, list):
            continue
        for dependency in dependencies:
            if not is_nonempty_string(dependency):
                continue
            if dependency == unit_id:
                add(diags, "error", f"units[{index}].depends_on", "self-dependency is invalid")
            elif dependency not in id_set:
                add(
                    diags,
                    "error",
                    f"units[{index}].depends_on",
                    f"unknown dependency: {dependency}",
                )
            else:
                graph[dependency].append(unit_id)
                indegree[unit_id] += 1

    queue = deque(unit_id for unit_id, degree in indegree.items() if degree == 0)
    visited = 0
    while queue:
        current = queue.popleft()
        visited += 1
        for successor in graph[current]:
            indegree[successor] -= 1
            if indegree[successor] == 0:
                queue.append(successor)
    if visited != len(id_set):
        add(diags, "error", "units", "dependency graph contains a cycle")

    if not isinstance(order, list) or not all(is_nonempty_string(item) for item in order):
        add(diags, "error", "landing_order", "must be an array containing every unit ID once")
        return
    if len(order) != len(id_set) or set(order) != id_set:
        add(diags, "error", "landing_order", "must contain every unit ID exactly once")
        return
    position = {unit_id: index for index, unit_id in enumerate(order)}
    for index, unit in enumerate(units):
        if not isinstance(unit, dict) or ids[index] is None:
            continue
        for dependency in unit.get("depends_on", []):
            if dependency in position and position[dependency] > position[ids[index]]:
                add(
                    diags,
                    "error",
                    "landing_order",
                    f"{dependency} must land before {ids[index]}",
                )


def validate_cleanup(units: list[Any], diags: list[dict[str, str]]) -> None:
    cleanup_for = {
        unit.get("contract_for")
        for unit in units
        if isinstance(unit, dict) and unit.get("delivery_strategy") == "contract"
    }
    for index, unit in enumerate(units):
        if not isinstance(unit, dict):
            continue
        if unit.get("delivery_strategy") in {"expand", "flag", "branch-by-abstraction"}:
            unit_id = unit.get("id")
            if unit_id not in cleanup_for:
                add(
                    diags,
                    "warning",
                    f"units[{index}].delivery_strategy",
                    "add a contract/removal unit referencing this temporary compatibility step",
                )


def validate(plan: Any, threshold_override: float | None) -> list[dict[str, str]]:
    diags: list[dict[str, str]] = []
    if not isinstance(plan, dict):
        return [{"severity": "error", "path": "$", "message": "plan must be a JSON object"}]
    if not is_nonempty_string(plan.get("goal")):
        add(diags, "error", "goal", "must be a non-empty string")

    threshold = threshold_override
    if threshold is None:
        threshold = plan.get("warning_line_threshold", 400)
    if not (
        isinstance(threshold, (int, float))
        and not isinstance(threshold, bool)
        and threshold > 0
    ):
        add(
            diags,
            "error",
            "warning_line_threshold",
            "must be a positive number",
        )
        threshold = 400

    units = plan.get("units")
    if not isinstance(units, list) or not units:
        add(diags, "error", "units", "must be a non-empty array")
        return diags

    ids = [validate_unit(unit, index, threshold, diags) for index, unit in enumerate(units)]
    validate_graph(units, ids, plan.get("landing_order"), diags)
    validate_cleanup(units, diags)
    return diags


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path, help="path to split-plan JSON")
    parser.add_argument(
        "--warning-lines",
        type=float,
        help="override the plan's warning line threshold",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="return failure when warnings exist",
    )
    parser.add_argument(
        "--json-output",
        action="store_true",
        help="emit diagnostics as JSON",
    )
    args = parser.parse_args()

    try:
        plan = json.loads(args.plan.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR {args.plan}: {exc}", file=sys.stderr)
        return 1

    diagnostics = validate(plan, args.warning_lines)
    errors = sum(item["severity"] == "error" for item in diagnostics)
    warnings = sum(item["severity"] == "warning" for item in diagnostics)

    if args.json_output:
        print(
            json.dumps(
                {"errors": errors, "warnings": warnings, "diagnostics": diagnostics},
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        for item in diagnostics:
            print(f"{item['severity'].upper()} {item['path']}: {item['message']}")
        print(f"Validation complete: {errors} error(s), {warnings} warning(s)")

    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
