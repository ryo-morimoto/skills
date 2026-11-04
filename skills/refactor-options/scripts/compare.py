#!/usr/bin/env python3
"""Read-only deterministic contract validator and cost/capacity calculator.

Only Python's standard library and bundled schema/template are used. No target
repository modules, expressions, network, subprocesses, or file writes.
"""

import argparse
import copy
import html
import itertools
import json
import math
from pathlib import Path
import re
import sys


ASSETS = Path(__file__).resolve().parent.parent / "assets"
FORMULA_VERSION = "1.0"
SCENARIOS = ("low", "reference", "high")
KEYWORDS = {"$schema", "$ref", "$defs", "type", "required", "properties",
            "additionalProperties", "items", "minItems", "maxItems", "minLength",
            "minimum", "maximum", "pattern", "enum", "const", "description", "title"}


class ContractError(ValueError):
    def __init__(self, code, path, message):
        super().__init__(message)
        self.code, self.path, self.message = code, path, message


def require(condition, code, path, message):
    if not condition:
        raise ContractError(code, path, message)


def pairs_unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate_key", "$", "Duplicate JSON key: " + key)
        result[key] = value
    return result


def reject_constant(value):
    raise ContractError("nonfinite", "$", "Non-finite JSON number: " + value)


def finite_tree(value, path="$"):
    if isinstance(value, float):
        require(math.isfinite(value), "nonfinite", path, "Numbers must be finite")
    elif isinstance(value, dict):
        for key, child in value.items():
            require(isinstance(key, str), "type", path, "Object keys must be strings")
            finite_tree(child, path + "." + key)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            finite_tree(child, f"{path}[{index}]")


def loads(text):
    try:
        value = json.loads(text, object_pairs_hook=pairs_unique, parse_constant=reject_constant)
    except json.JSONDecodeError as exc:
        raise ContractError("json", "$", str(exc)) from None
    finite_tree(value)
    return value


def audit_schema(node, root, path="$"):
    """Fail closed on keywords outside the deliberately limited local subset."""
    require(isinstance(node, dict), "schema", path, "Schema must be an object")
    require(not set(node) - KEYWORDS, "schema", path,
            "Unsupported schema keywords: " + ", ".join(sorted(set(node) - KEYWORDS)))
    if "$ref" in node:
        require(set(node) <= {"$ref", "$schema", "$defs", "description", "title"},
                "schema", path, "$ref siblings with validation semantics are unsupported")
        ref = node["$ref"]
        require(isinstance(ref, str) and ref.startswith("#/$defs/") and
                ref[8:] in root.get("$defs", {}), "schema", path, "Only bundled $defs references are supported")
    if "type" in node:
        types = node["type"] if isinstance(node["type"], list) else [node["type"]]
        require(all(t in {"object", "array", "string", "number", "integer", "boolean", "null"} for t in types),
                "schema", path, "Unsupported type")
    if "additionalProperties" in node:
        require(type(node["additionalProperties"]) is bool, "schema", path, "Only boolean additionalProperties is supported")
    for keyword in ("$defs", "properties"):
        for key, child in node.get(keyword, {}).items():
            audit_schema(child, root, path + "." + keyword + "." + key)
    if "items" in node:
        audit_schema(node["items"], root, path + ".items")


def load_schema():
    schema = loads((ASSETS / "decision.schema.json").read_text(encoding="utf-8"))
    audit_schema(schema, schema)
    return schema


def matches_type(value, kind):
    return {"object": lambda: isinstance(value, dict),
            "array": lambda: isinstance(value, list),
            "string": lambda: isinstance(value, str),
            "number": lambda: type(value) in (int, float),
            "integer": lambda: type(value) is int,
            "boolean": lambda: type(value) is bool,
            "null": lambda: value is None}[kind]()


def schema_validate(value, node, root, path="$"):
    if "$ref" in node:
        return schema_validate(value, root["$defs"][node["$ref"][8:]], root, path)
    if "type" in node:
        kinds = node["type"] if isinstance(node["type"], list) else [node["type"]]
        require(any(matches_type(value, kind) for kind in kinds), "type", path, "Expected " + "/".join(kinds))
    if "const" in node:
        require(type(value) is type(node["const"]) and value == node["const"], "const", path, "Unexpected constant")
    if "enum" in node:
        require(any(type(value) is type(item) and value == item for item in node["enum"]), "enum", path, "Unexpected enum value")
    if isinstance(value, dict):
        props = node.get("properties", {})
        require(not set(node.get("required", [])) - set(value), "required", path,
                "Missing fields: " + ", ".join(sorted(set(node.get("required", [])) - set(value))))
        if node.get("additionalProperties") is False:
            require(not set(value) - set(props), "additional_property", path,
                    "Unknown fields: " + ", ".join(sorted(set(value) - set(props))))
        for key in sorted(set(value) & set(props)):
            schema_validate(value[key], props[key], root, path + "." + key)
    if isinstance(value, list):
        require(len(value) >= node.get("minItems", 0), "length", path, "Too few items")
        if "maxItems" in node:
            require(len(value) <= node["maxItems"], "length", path, "Too many items")
        if "items" in node:
            for index, item in enumerate(value):
                schema_validate(item, node["items"], root, f"{path}[{index}]")
    if isinstance(value, str):
        require(len(value) >= node.get("minLength", 0), "length", path, "String is empty")
        if "pattern" in node:
            require(re.search(node["pattern"], value) is not None, "pattern", path, "String does not match pattern")
    if type(value) in (int, float):
        if "minimum" in node:
            require(value >= node["minimum"], "minimum", path, "Number below minimum")
        if "maximum" in node:
            require(value <= node["maximum"], "maximum", path, "Number above maximum")


def unique(items, field, path):
    values = [item[field] for item in items]
    require(len(values) == len(set(values)), "duplicate_id", path, "Duplicate " + field)
    return set(values)


def range_check(value, path, unit=None):
    if unit:
        require(value["unit"] == unit, "unit", path, "Expected unit " + unit)
    values = [value[key] for key in SCENARIOS]
    require(all(v is None for v in values) or all(v is not None for v in values),
            "range", path, "Range must be all known or all null")
    if values[0] is None:
        require(bool(value["reason"].strip()), "unknown_reason", path, "Unknown range requires a reason")
    else:
        require(values[0] <= values[1] <= values[2], "range", path, "Expected low <= reference <= high")
        require(bool(value["evidence_ids"] or value["assumption_ids"]), "basis", path,
                "Known range requires evidence or assumption IDs")


def semantic_walk(value, path="$"):
    if isinstance(value, dict):
        if {"unit", "low", "reference", "high", "basis", "evidence_ids", "assumption_ids", "reason"} <= set(value):
            range_check(value, path)
        for key, item in value.items():
            if key in ("evidence_ids", "assumption_ids", "unknown_ids", "depends_on"):
                require(len(item) == len(set(item)), "duplicate_id", path + "." + key, "Duplicate reference")
            semantic_walk(item, path + "." + key)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            semantic_walk(item, f"{path}[{index}]")


def context_check(context):
    for field in ("constraints", "evidence", "assumptions", "unknowns"):
        unique(context[field], "id", "$.context." + field)
    unique(context["snapshot"]["files"], "path", "$.context.snapshot.files")


def plan_check(plan, path):
    unique(plan["costs"], "id", path + ".costs")
    unique(plan["risks"], "id", path + ".risks")
    unique(plan["gates"], "constraint_id", path + ".gates")
    ids = unique(plan["steps"], "id", path + ".steps")
    dependencies = {step["id"]: step["depends_on"] for step in plan["steps"]}
    for step in plan["steps"]:
        require(set(step["depends_on"]) <= ids, "reference", path + ".steps", "Unknown step dependency")
    # Kahn's algorithm accepts forward references, rejects cycles, and does not recurse.
    done = set()
    while len(done) < len(ids):
        ready = {key for key in ids - done if set(dependencies[key]) <= done}
        require(bool(ready), "cycle", path + ".steps", "Cyclic step dependencies")
        done.update(ready)
    for cost in plan["costs"]:
        range_check(cost["hours"], path + ".costs." + cost["id"], "person_hour")
    range_check(plan["recovery"]["hours"], path + ".recovery.hours", "person_hour")
    for risk in plan["risks"]:
        range_check(risk["recovery_hours"], path + ".risks." + risk["id"], "person_hour")
    range_check(plan["monthly_savings_hours"], path + ".monthly_savings_hours", "person_hour/month")
    range_check(plan["completion_months"], path + ".completion_months", "month")


def reference_walk(value, registries, path="$"):
    if isinstance(value, dict):
        for key, item in value.items():
            if key in registries:
                require(set(item) <= registries[key], "reference", path + "." + key, "Unknown referenced ID")
            reference_walk(item, registries, path + "." + key)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            reference_walk(item, registries, f"{path}[{index}]")


def admissibility(packet, plan):
    constraints = {item["id"] for item in packet["context"]["constraints"]}
    gates = {gate["constraint_id"]: gate["status"] for gate in plan["gates"]}
    findings = [f for f in packet["critique"]["findings"] if f["plan_id"] in (None, plan["id"])]
    design = next((review["status"] for review in packet["critique"].get("design_review", {}).get("plans", [])
                   if review["plan_id"] == plan["id"]), None)
    if design == "invalid" or plan["status"] == "infeasible" or "fail" in gates.values() or any(f["severity"] == "blocking" for f in findings):
        return "excluded"
    if design in ("conditional", "unknown") or plan["status"] == "incomplete" or constraints - set(gates) or "unknown" in gates.values() or any(f["severity"] == "major" for f in findings):
        return "conditional"
    return "admissible"


def design_plan_check(review, path):
    # The schema limits criteria to six values and requires exactly six checks.
    unique(review["checks"], "criterion", path + ".checks")
    statuses = {check["status"] for check in review["checks"]}
    status = review["status"]
    consistent = {"plausible": statuses == {"pass"},
                  "invalid": "fail" in statuses,
                  "conditional": "fail" not in statuses and bool(statuses & {"conditional", "unknown"}),
                  "unknown": "fail" not in statuses and "unknown" in statuses}
    require(consistent[status], "design_verdict", path, "Design verdict contradicts planning checks")


def design_pair_check(pair, path):
    require(len(set(pair["plan_ids"])) == 2, "duplicate_id", path + ".plan_ids", "Pair requires two different plan IDs")
    require(all(axis["difference"].strip() for axis in pair["axes"]),
            "design_axis", path + ".axes", "Difference must be substantive, not blank")
    if pair["status"] in ("distinct", "overlapping"):
        require(bool(pair["axes"]), "design_axis", path + ".axes", "Distinct/overlapping requires a substantive difference axis")


def design_review_check(review, plan_ids=None, path="$"):
    ids = unique(review["plans"], "plan_id", path + ".plans")
    expected = ids if plan_ids is None else plan_ids
    require("P0" in expected and ids == expected, "reference", path + ".plans",
            "Design review must cover P0 and every reviewed plan exactly once")
    for index, plan in enumerate(review["plans"]):
        design_plan_check(plan, f"{path}.plans[{index}]")
    pairs = set()
    for index, pair in enumerate(review["pairwise"]):
        pair_path = f"{path}.pairwise[{index}]"
        design_pair_check(pair, pair_path)
        key = frozenset(pair["plan_ids"])
        require(key <= expected - {"P0"}, "reference", pair_path, "Pair must reference change plans only; P0 is excluded")
        require(key not in pairs, "duplicate_id", pair_path, "Duplicate or reversed pair")
        pairs.add(key)
    required_pairs = {frozenset(pair) for pair in itertools.combinations(sorted(expected - {"P0"}), 2)}
    require(pairs == required_pairs, "design_coverage", path + ".pairwise", "Review must cover every unordered pair of change plans")


def nonblank_tree(value, path):
    """New planning text must contain content; leave legacy text rules intact."""
    if isinstance(value, str):
        require(bool(value.strip()), "blank", path, "Text must not be whitespace-only")
    elif isinstance(value, dict):
        for key, item in value.items():
            nonblank_tree(item, path + "." + key)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            nonblank_tree(item, f"{path}[{index}]")


def planning_check(planning, plan_ids=None, path="$"):
    nonblank_tree(planning, path)
    areas = unique(planning["areas"], "id", path + ".areas")
    assignments = planning["assignments"]
    ids = unique(assignments, "plan_id", path + ".assignments")
    expected = ids if plan_ids is None else plan_ids
    require("P0" not in ids and ids == expected, "reference", path + ".assignments",
            "Assign every change plan exactly once, never P0")
    alternatives = planning["mode"] == "alternatives"
    require(len(areas) == 1 if alternatives else len(areas) >= 2, "planning_mode", path + ".areas",
            "Alternatives require exactly one area; portfolio requires at least two")
    covered = set()
    dependencies = {}
    for index, item in enumerate(assignments):
        item_path = f"{path}.assignments[{index}]"
        assigned = item["area_ids"]
        require(len(assigned) == len(set(assigned)), "duplicate_id", item_path + ".area_ids", "Duplicate area ID")
        require(set(assigned) <= areas, "reference", item_path + ".area_ids", "Unknown area ID")
        covered.update(assigned)
        dependencies[item["plan_id"]] = set(item["depends_on"])
        require(set(item["depends_on"]) <= expected - {item["plan_id"], "P0"}, "reference",
                item_path + ".depends_on", "Dependencies must be other known change plans, never P0")
        require(not alternatives or not item["depends_on"], "planning_mode", item_path + ".depends_on",
                "Alternatives cannot have prerequisites")
    require(covered == areas, "planning_coverage", path + ".areas", "Every declared area needs a candidate")
    done = set()
    while len(done) < len(ids):
        ready = {key for key in ids - done if dependencies[key] <= done}
        require(bool(ready), "cycle", path + ".assignments", "Cyclic plan prerequisites")
        done.update(ready)
    pairs = set()
    for index, relation in enumerate(planning["relations"]):
        pair_path = f"{path}.relations[{index}]"
        pair = frozenset(relation["plan_ids"])
        require(len(pair) == 2, "duplicate_id", pair_path + ".plan_ids", "Pair requires two distinct change plans")
        require(pair <= expected - {"P0"}, "reference", pair_path, "Relation must reference change plans only")
        require(pair not in pairs, "duplicate_id", pair_path, "Duplicate or reversed relation pair")
        pairs.add(pair)
        require(not alternatives or relation["relationship"] == "alternative", "planning_mode", pair_path,
                "All relations in alternatives mode must be alternative")
    required_pairs = {frozenset(pair) for pair in itertools.combinations(sorted(expected), 2)}
    require(pairs == required_pairs, "planning_coverage", path + ".relations",
            "Relations must cover every unordered pair of change plans")


def portfolio_selection_check(packet, field, by_id):
    selection = packet[field]
    path = "$." + field
    require("plan_ids" in selection, "required", path, "Portfolio requires explicit plan_ids (may be empty)")
    require(selection["plan_id"] is None, "selection", path, "Portfolio plan_id must be null; use plan_ids only")
    chosen = selection["plan_ids"]
    require(len(chosen) == len(set(chosen)), "duplicate_id", path + ".plan_ids", "Duplicate selected plan ID")
    chosen = set(chosen)
    require(chosen <= set(by_id) - {"P0"}, "reference", path + ".plan_ids", "Select known change plans only, never P0")
    require(all(admissibility(packet, by_id[plan_id]) != "excluded" for plan_id in chosen),
            "excluded", path, "Excluded plans cannot be selected or recommended")
    for assignment in packet["planning"]["assignments"]:
        if assignment["plan_id"] in chosen:
            require(set(assignment["depends_on"]) <= chosen, "prerequisite", path,
                    "Portfolio must include prerequisite closure")
    unknown = False
    for relation in packet["planning"]["relations"]:
        if set(relation["plan_ids"]) <= chosen:
            require(relation["compatibility"] != "conflicting" and relation["relationship"] != "alternative",
                    "selection", path, "Conflicting or alternative plans cannot be chosen together")
            unknown |= relation["compatibility"] == "unknown"
    if field == "recommendation" and (unknown or any(admissibility(packet, by_id[p]) == "conditional" for p in chosen)):
        require(bool(selection["conditions"]) and all(condition.strip() for condition in selection["conditions"]),
                "recommendation", path, "Conditional plans or unknown compatibility require nonblank explicit conditions")
    return chosen


def selection_check(packet, ids, by_id):
    decision = packet["decision"]
    portfolio = packet["schema_version"] == "1.1" and packet["planning"]["mode"] == "portfolio"
    for field in ("decision", "recommendation"):
        if portfolio:
            chosen = portfolio_selection_check(packet, field, by_id)
        else:
            require(not packet[field].get("plan_ids"), "selection", "$." + field,
                    "Alternatives use single plan_id; plan_ids must be absent or empty")
            single = packet[field]["plan_id"]
            require(single is None or single in ids, "reference", "$." + field, "Unknown plan ID")
            chosen = set() if single is None else {single}
            if chosen:
                require(admissibility(packet, by_id[single]) != "excluded", "excluded", "$." + field,
                        "Excluded plans cannot be selected or recommended")
        if field == "decision":
            if decision["status"] == "pending":
                require(decision["answer"] is None and not chosen, "decision", "$.decision", "Pending means no human answer or selection")
            else:
                require(isinstance(decision["answer"], str) and bool(decision["answer"].strip()),
                        "decision", "$.decision", "Explicit human answer required")
                require((decision["status"] == "selected") == bool(chosen), "decision", "$.decision",
                        "Only selected has one or more chosen plans")
        elif not portfolio and chosen and admissibility(packet, by_id[single]) == "conditional":
            conditions = packet["recommendation"]["conditions"]
            require(bool(conditions), "recommendation", "$.recommendation", "Conditional recommendation requires explicit conditions")
            if packet["schema_version"] == "1.1":
                require(all(condition.strip() for condition in conditions), "recommendation", "$.recommendation",
                        "Conditions must be nonblank")


def packet_check(packet):
    context = packet["context"]
    if packet["schema_version"] == "1.1":
        require(context["schema_version"] == "1.1", "version", "$.context.schema_version", "Packet 1.1 requires context 1.1")
        require("planning" in packet, "required", "$", "Packet 1.1 requires planning")
        require("design_review" in packet["critique"], "required", "$.critique", "Packet 1.1 requires design_review")
        require(len(packet["plans"]) >= 3, "plan_count", "$.plans", "Need at least three change proposals; P0 does not count")
    else:
        require(2 <= len(packet["plans"]) <= 3, "plan_count", "$.plans", "Legacy 1.0 requires two to three change proposals")
        require("planning" not in packet and all("plan_ids" not in packet[field] for field in ("decision", "recommendation")),
                "version", "$", "Planning and multi-selection fields require schema 1.1")
    context_check(context)
    revision = context["context_revision"]
    plans = [packet["baseline"]] + packet["plans"]
    ids = unique(plans, "id", "$.plans")
    baseline = packet["baseline"]
    require(baseline["id"] == "P0" and baseline["strategy_id"] == "baseline", "baseline", "$.baseline", "Baseline must be P0 / baseline")
    if packet["schema_version"] == "1.1":
        planning_check(packet["planning"], ids - {"P0"}, "$.planning")
    strategies = unique(packet["plans"], "strategy_id", "$.plans")
    require("baseline" not in strategies, "baseline", "$.plans", "Alternative cannot use baseline strategy")
    for plan in plans:
        require(plan["context_revision"] == revision, "stale", "$.plans." + plan["id"], "Stale plan context revision")
        plan_check(plan, "$.plans." + plan["id"])
    require(bool(baseline["costs"]), "baseline", "$.baseline.costs", "Baseline requires explicit zero delta cost")
    for value in [c["hours"] for c in baseline["costs"]] + [baseline["monthly_savings_hours"], baseline["completion_months"]]:
        require(all(value[key] == 0 for key in SCENARIOS), "baseline", "$.baseline", "Baseline delta cost, savings and completion must be known zero")
    critique = packet["critique"]
    require(critique["context_revision"] == revision, "stale", "$.critique", "Stale critique context revision")
    reviewed = unique(critique["reviewed_plans"], "plan_id", "$.critique.reviewed_plans")
    require(reviewed == ids, "reference", "$.critique.reviewed_plans", "Critic must review baseline and all alternatives")
    by_id = {plan["id"]: plan for plan in plans}
    for item in critique["reviewed_plans"]:
        require(item["plan_revision"] == by_id[item["plan_id"]]["plan_revision"], "stale", "$.critique", "Stale reviewed plan revision")
    if "design_review" in critique:
        design_review_check(critique["design_review"], reviewed, "$.critique.design_review")
    unique(critique["findings"], "id", "$.critique.findings")
    for finding in critique["findings"]:
        require(finding["plan_id"] is None or finding["plan_id"] in ids, "reference", "$.critique.findings", "Unknown finding plan")
    registries = {field + "_ids": {item["id"] for item in context[source]}
                  for field, source in (("evidence", "evidence"), ("assumption", "assumptions"), ("unknown", "unknowns"))}
    # Computed data is checked separately; it is never treated as source evidence.
    reference_walk({key: value for key, value in packet.items() if key != "assessment"}, registries)
    constraints = {item["id"] for item in context["constraints"]}
    for plan in plans:
        require({gate["constraint_id"] for gate in plan["gates"]} <= constraints, "reference", "$.plans." + plan["id"], "Unknown constraint ID")
    decision = packet["decision"]
    require(decision["context_revision"] == revision, "stale", "$.decision", "Stale decision context revision")
    selection_check(packet, ids, by_id)
    records = packet["run_record"]
    unique(records, "call_id", "$.run_record")
    for record in records:
        require(record["context_revision"] == revision, "stale", "$.run_record", "Run records must use current context revision")
        require((record["role"] == "critic" and record["strategy_id"] is None) or
                (record["role"] == "planner" and record["strategy_id"] in strategies),
                "reference", "$.run_record", "Run role/strategy does not align with alternatives")
    planners = [r for r in records if r["role"] == "planner" and r["status"] == "completed"]
    critics = [r for r in records if r["role"] == "critic" and r["status"] == "completed"]
    # One completed initial batch must cover every strategy in independent contexts.
    batches = {r["batch_id"] for r in planners}
    valid_batches = []
    for batch in batches:
        group = [r for r in planners if r["batch_id"] == batch]
        if {r["strategy_id"] for r in group} == strategies and len({r["context_id"] for r in group}) == len(group) and len(group) == len(strategies):
            valid_batches.append(group)
    require(bool(valid_batches), "trace", "$.run_record", "Need independent completed planners covering every change strategy in the same batch")
    require(any(c["context_id"] not in {p["context_id"] for p in planners} for c in critics),
            "trace", "$.run_record", "Need an independent completed critic context")


def validate(value, type_name="decision_packet", schema=None):
    schema = schema if schema is not None else load_schema()
    audit_schema(schema, schema)
    require(type_name in schema["$defs"], "type", "$", "Unknown contract type")
    finite_tree(value)
    schema_validate(value, schema["$defs"][type_name], schema)
    semantic_walk(value)
    if type_name == "decision_packet":
        packet_check(value)
    elif type_name == "shared_context":
        context_check(value)
    elif type_name == "plan_result":
        plan_check(value, "$")
    elif type_name == "critique_result":
        reviewed = unique(value["reviewed_plans"], "plan_id", "$.reviewed_plans")
        unique(value["findings"], "id", "$.findings")
        if "design_review" in value:
            # Standalone critiques have plan IDs, but no source revisions or
            # evidence registry. Those external references need packet_check.
            design_review_check(value["design_review"], reviewed, "$.design_review")
            for finding in value["findings"]:
                require(finding["plan_id"] is None or finding["plan_id"] in reviewed,
                        "reference", "$.findings", "Unknown finding plan")
    elif type_name == "design_review":
        design_review_check(value)
    elif type_name == "design_plan_review":
        design_plan_check(value, "$")
    elif type_name == "design_pair":
        design_pair_check(value, "$")
    elif type_name == "planning":
        # Assignment IDs are only a local authority. External plan/evidence
        # registries and minimum packet count require decision_packet validation.
        planning_check(value)
    elif type_name in ("planning_area", "planning_assignment", "planning_relation"):
        nonblank_tree(value, "$")
    return value


def cost_summary(plan):
    known = [cost for cost in plan["costs"] if cost["hours"]["reference"] is not None]
    missing = sorted(cost["id"] for cost in plan["costs"] if cost["hours"]["reference"] is None)
    complete = bool(plan["costs"]) and not missing
    subtotal = {key: sum(cost["hours"][key] for cost in sorted(known, key=lambda c: c["id"])) for key in SCENARIOS}
    return {"unit": "person_hour", "status": "complete" if complete else "incomplete",
            "known_subtotal": subtotal, "total": subtotal.copy() if complete else None,
            "unknown_component_ids": missing, "empty_components": not bool(plan["costs"])}


def capacity(plan, cost, horizon):
    savings, completion = plan["monthly_savings_hours"], plan["completion_months"]
    missing = []
    if horizon is None:
        missing.append("horizon_months")
    if cost["total"] is None:
        missing.append("cost_total")
    for name in ("monthly_savings_hours", "completion_months"):
        if plan[name]["reference"] is None:
            missing.append(name)
    if missing:
        return {"status": "unknown", "unit": "person_hour", "values": None, "missing": missing}
    # Bounds combine pessimistic/optimistic inputs, not probabilities or quantiles.
    values = {
        "low": savings["low"] * max(0, horizon - completion["high"]) - cost["total"]["high"],
        "reference": savings["reference"] * max(0, horizon - completion["reference"]) - cost["total"]["reference"],
        "high": savings["high"] * max(0, horizon - completion["low"]) - cost["total"]["low"]}
    finite_tree(values)
    return {"status": "known", "unit": "person_hour", "values": values, "missing": []}


def compute_assessment(packet, horizons=None):
    horizon = packet["context"]["horizon_months"]
    if horizons is None:
        horizons = [] if horizon is None else [max(0, horizon - 1), horizon, horizon + 1]
    require(all(type(h) in (int, float) and math.isfinite(h) and h >= 0 for h in horizons), "horizon", "$", "Sensitivity horizons must be finite nonnegative numbers")
    horizons = sorted(set(horizons))
    plans = sorted([packet["baseline"]] + packet["plans"], key=lambda p: p["id"])
    rows = []
    for plan in plans:
        cost = cost_summary(plan)
        severities = [risk["residual_severity"] for risk in plan["risks"] if risk["residual_severity"] is not None]
        maximum = max(severities) if severities else None
        rows.append({"plan_id": plan["id"], "admissibility": admissibility(packet, plan), "cost": cost,
                     "capacity": capacity(plan, cost, horizon),
                     "missing_gate_ids": sorted({c["id"] for c in packet["context"]["constraints"]} - {g["constraint_id"] for g in plan["gates"]}),
                     "maximum_identified_residual_severity": maximum,
                     "maximum_severity_risk_ids": sorted(r["id"] for r in plan["risks"] if maximum is not None and r["residual_severity"] == maximum),
                     "unknown_severity_risk_ids": sorted(r["id"] for r in plan["risks"] if r["residual_severity"] is None)})
    costs = {row["plan_id"]: row["cost"] for row in rows}
    break_even = []
    for left, right in itertools.combinations(plans, 2):
        item = {"plan_ids": [left["id"], right["id"]], "status": "unknown", "horizon_months": None,
                "reason": "Missing reference inputs"}
        if (packet["schema_version"] == "1.1" and packet["planning"]["mode"] == "portfolio" and
                "P0" not in item["plan_ids"]):
            item.update(status="not_comparable", reason="Portfolio change plans have different/nonexclusive objectives; standalone incremental capacities are not competing alternatives or a combined estimate")
            break_even.append(item)
            continue
        inputs = []
        for plan in (left, right):
            total = costs[plan["id"]]["total"]
            inputs.append(None if total is None or plan["monthly_savings_hours"]["reference"] is None or plan["completion_months"]["reference"] is None else
                          (plan["monthly_savings_hours"]["reference"], plan["completion_months"]["reference"], total["reference"]))
        if all(value is not None for value in inputs):
            (b1, m1, c1), (b2, m2, c2) = inputs
            if b1 == b2:
                item.update(status="coincident_reference_lines" if b1 * m1 + c1 == b2 * m2 + c2 else "no_crossing", reason="Equal reference slopes; only valid after both completion times")
            else:
                crossing = (b1 * m1 + c1 - b2 * m2 - c2) / (b1 - b2)
                if crossing >= max(0, m1, m2):
                    item.update(status="known", horizon_months=crossing, reason="Reference lines only, after both completion times; not a risk-adjusted preference")
                else:
                    item.update(status="outside_domain", reason="Reference-line intersection precedes completion; no valid post-completion crossing")
        break_even.append(item)
    result = {"formula_version": FORMULA_VERSION, "horizon_months": horizon,
              "scenario_semantics": "Cost components add by low/reference/high scenario; capacity low/high combine adverse/favorable inputs. No probabilities, cash ROI, risk score, or universal dominance.",
              "plans": rows, "sensitivity_horizons": horizons,
              "sensitivity": [{"horizon_months": h, "plans": [{"plan_id": p["id"], "capacity": capacity(p, costs[p["id"]], h)} for p in plans]} for h in horizons],
              "reference_break_even": break_even}
    finite_tree(result)
    return result


def verify_assessment(packet):
    if "assessment" in packet:
        supplied = packet["assessment"]
        require(isinstance(supplied.get("sensitivity_horizons"), list), "assessment", "$.assessment", "Missing sensitivity horizons")
        expected = compute_assessment(packet, supplied["sensitivity_horizons"])
        require(canonical(supplied) == canonical(expected), "assessment", "$.assessment", "Stale or tampered assessment; recompute from raw inputs")


def compare(packet, horizons=None):
    validate(packet)
    verify_assessment(packet)
    result = copy.deepcopy(packet)
    result["assessment"] = compute_assessment(packet, horizons)
    return result


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False, separators=(",", ":"))


def escape(value):
    text = "unknown" if value is None else str(value)
    return html.escape(text, quote=False).translate(str.maketrans({
        "|": "&#124;", "`": "&#96;", "\r": "&#13;", "\n": "&#10;", "*": "&#42;",
        "_": "&#95;", "[": "&#91;", "]": "&#93;", "#": "&#35;", "\\": "&#92;"}))


def tree(value, depth=0):
    """Lossless labelled raw fields, escaped before insertion into Markdown."""
    lines = []
    if isinstance(value, dict):
        for key, item in value.items():
            if isinstance(item, (dict, list)) and item:
                lines.append("  " * depth + "- " + escape(key) + ":")
                lines.extend(tree(item, depth + 1))
            else:
                lines.append("  " * depth + "- " + escape(key) + ": " + escape(canonical(item) if isinstance(item, (dict, list)) else item))
    elif isinstance(value, list):
        for item in value:
            if isinstance(item, (dict, list)):
                lines.append("  " * depth + "- Item:")
                lines.extend(tree(item, depth + 1))
            else:
                lines.append("  " * depth + "- " + escape(item))
    return lines


def render_planning(packet):
    count = len(packet["plans"])
    if packet["schema_version"] == "1.0":
        return ("Legacy 1.0 count/mode warning: " + escape(count) +
                " change proposals (P0 excluded); the historical two-to-three contract is preserved, "
                "not upgraded to the current minimum of three. Planning mode/areas/relations were not supplied; "
                "legacy single-plan comparison does not establish portfolio compatibility or independence.")
    planning = packet["planning"]
    statuses = {status: sum(plan["status"] == status for plan in packet["plans"])
                for status in ("viable", "infeasible", "incomplete")}
    eligible = {status: sum(admissibility(packet, plan) == status for plan in packet["plans"])
                for status in ("admissible", "conditional", "excluded")}
    lines = ["Mode: " + escape(planning["mode"]) + ". Change proposals: " + escape(count) + " (P0 excluded).",
             "Declared status: " + ", ".join(escape(key) + "=" + escape(value) for key, value in statuses.items()) + ".",
             "Gate/design admissibility: " + ", ".join(escape(key) + "=" + escape(value) for key, value in eligible.items()) + ".",
             "Attempted infeasible candidates count structurally, not as viable choices. Design duplicates do not establish three valid independent options.",
             "Different areas do not imply independence or disjoint benefits. Relations are review assertions, separate from design diversity."]
    if planning["mode"] == "portfolio":
        lines.append("Portfolio Diversity is not proof of competing alternatives. Per-plan capacity is standalone incremental capacity against P0, not a portfolio estimate.")
    lines.extend(["No combined estimate: do not sum raw plan costs/benefits/capacities into a set total; overlap, prerequisites and interactions are unresolved by this calculator. No universal ranking or automatic selection.",
                  "", *tree(planning)])
    for relation in planning["relations"]:
        pair = escape(" / ".join(relation["plan_ids"]))
        compatibility = relation["compatibility"]
        if compatibility == "compatible":
            message = "Compatible assertion, not proof of safe composition or additive benefits"
        elif compatibility == "conflicting":
            message = "Conflicting warning: these plans cannot be recommended or selected together"
        else:
            message = "Unknown compatibility warning: safety is not established; this alone does not prohibit joint selection, but alternative/conflicting pairs remain prohibited"
        lines.extend(["", message + ": " + pair + "."])
        if relation["relationship"] == "alternative":
            lines.append("Alternative-pair warning: joint selection is prohibited: " + pair + ".")
        if compatibility == "unknown":
            for field in ("recommendation", "decision"):
                if set(relation["plan_ids"]) <= set(packet[field].get("plan_ids", [])):
                    lines.append(escape(field) + " includes unknown compatibility: " + pair + "; safety is not established.")
    return "\n".join(lines)


def render_design(critique, mode=None):
    review = critique.get("design_review")
    if review is None:
        return ("Design evaluation not supplied (design review missing). Meaningful differences and individual "
                "architectural plausibility are not retroactively validated. Existing raw results and admissibility are unchanged.")
    lines = ["Static planning plausibility, not executed test success or a universal architecture score. "
             "Unmeasured cost alone does not invalidate architecture. P0 is a deliberate no-change reference, "
             "not invalid merely because it does not improve the objective.", "",
             "| Change-plan pair | Diversity | Axes / evidence | Reason |",
             "| --- | --- | --- | --- |"]
    for pair in sorted(review["pairwise"], key=lambda p: sorted(p["plan_ids"])):
        axes = "<br>".join(escape(axis["axis"] + ": " + axis["difference"] +
                                 " (evidence: " + (", ".join(axis["evidence_ids"]) or "none supplied") + ")")
                          for axis in pair["axes"]) or "none supplied"
        lines.append("| " + " | ".join([escape(" / ".join(pair["plan_ids"])), escape(pair["status"]), axes, escape(pair["reason"])]) + " |")
    for pair in review["pairwise"]:
        if pair["status"] == "duplicate":
            lines.extend(["", "Diversity warning: duplicate pair " + escape(" / ".join(pair["plan_ids"])) +
                          (" does not prove two distinct portfolio contributions; neither plan is automatically excluded."
                           if mode == "portfolio" else " does not count as two meaningful alternatives; neither plan is automatically excluded.")])
        elif pair["status"] == "unknown":
            lines.extend(["", "Diversity unresolved: " + escape(" / ".join(pair["plan_ids"])) + "; meaningful differences are not established."])
    lines.extend(["", "| Plan | Planning validity | Six checks / reasons / evidence | Unresolved conditions |",
                  "| --- | --- | --- | --- |"])
    for plan in sorted(review["plans"], key=lambda p: p["plan_id"]):
        checks = "<br>".join(escape(check["criterion"] + ": " + check["status"] + " — " + check["reason"] +
                                   " (evidence: " + (", ".join(check["evidence_ids"]) or "none supplied") + ")")
                            for check in plan["checks"])
        conditions = "<br>".join(escape(item) for item in plan["unresolved"]) or "none supplied"
        lines.append("| " + " | ".join([escape(plan["plan_id"]), escape(plan["status"]), checks, conditions]) + " |")
    return "\n".join(lines)


def render(packet):
    validate(packet)
    verify_assessment(packet)
    assessment = packet.get("assessment") or compute_assessment(packet)
    table = ["| Plan | Gate/feasibility | Cost total (low/ref/high person-hour) | Known subtotal | Net capacity (low/ref/high person-hour) | Max identified residual S (ordinal) |",
             "| --- | --- | --- | --- | --- | --- |"]
    def triple(value):
        return "unknown" if value is None else " / ".join(escape(value[k]) for k in SCENARIOS)
    for row in assessment["plans"]:
        table.append("| " + " | ".join([escape(row["plan_id"]), escape(row["admissibility"]), triple(row["cost"]["total"]),
                     triple(row["cost"]["known_subtotal"]) + " (" + row["cost"]["status"] + ")", triple(row["capacity"]["values"]),
                     escape(row["maximum_identified_residual_severity"])]) + " |")
    sections = {
        "context": "\n".join(tree(packet["context"])),
        "planning": render_planning(packet),
        "design": render_design(packet["critique"], packet.get("planning", {}).get("mode")),
        "comparison": "\n".join(table) + "\n\n" + "\n".join(tree({"formula_version": assessment["formula_version"], "horizon_months": assessment["horizon_months"], "scenario_semantics": assessment["scenario_semantics"], "details": assessment["plans"]})),
        "plans": "\n\n".join("### " + escape(p["id"]) + " — " + escape(p["name"]) + "\n\n" + "\n".join(tree(p)) for p in [packet["baseline"]] + sorted(packet["plans"], key=lambda p: p["id"])),
        "critique": "\n".join(tree(packet["critique"])),
        "sensitivity": "\n".join(tree({"sensitivity": assessment["sensitivity"], "reference_break_even": assessment["reference_break_even"]})),
        "decision": "\n".join(tree({"recommendation": packet["recommendation"], "decision": packet["decision"]})),
        "traces": "\n".join(tree(packet["run_record"]))}
    template = (ASSETS / "decision-template.md").read_text(encoding="utf-8")
    # One substitution pass: source strings cannot introduce template directives.
    return re.sub(r"\{\{([a-z]+)\}\}", lambda match: sections[match.group(1)], template)


def describe(type_name, schema):
    require(type_name in schema["$defs"], "type", "$", "Unknown contract type")
    needed = set()
    def visit(name):
        if name in needed:
            return
        needed.add(name)
        def walk(node):
            if isinstance(node, dict):
                if "$ref" in node:
                    visit(node["$ref"][8:])
                for item in node.values():
                    walk(item)
            elif isinstance(node, list):
                for item in node:
                    walk(item)
        walk(schema["$defs"][name])
    visit(type_name)
    return {"$schema": schema["$schema"], "$ref": "#/$defs/" + type_name,
            "$defs": {name: schema["$defs"][name] for name in sorted(needed)}}


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise ContractError("arguments", "$", message)


def main(argv=None):
    parser = Parser(description="Read-only stdin JSON validator/calculator. No implementation, ranking, automatic selection, network or target-repo imports.")
    subs = parser.add_subparsers(dest="command", required=True, parser_class=Parser)
    for command in ("validate", "describe"):
        sub = subs.add_parser(command, help="Validate JSON contract" if command == "validate" else "Print schema and transitive definitions (no stdin)")
        sub.add_argument("--type", required=True, help="Bundled $defs name, e.g. decision_packet, planning, shared_context, strategy_task, plan_result, critique_result, run_record, range, evidence")
    sub = subs.add_parser("compare", help="Validate and return packet with computed assessment")
    sub.add_argument("--horizons", nargs="+", type=float, help="Sensitivity months; default current H-1, H, H+1 (clamped at zero)")
    subs.add_parser("render", help="Verify/recompute assessment and print full Markdown report")
    args = parser.parse_args(argv)
    schema = load_schema()
    if args.command == "describe":
        result = describe(args.type, schema)
    else:
        packet = loads(sys.stdin.read())
        if args.command == "validate":
            validate(packet, args.type, schema)
            if args.type == "decision_packet":
                verify_assessment(packet)
            result = {"valid": True, "type": args.type, "schema_version": packet.get("schema_version", "1.0") if isinstance(packet, dict) else "1.0"}
        elif args.command == "compare":
            result = compare(packet, args.horizons)
        else:
            sys.stdout.write(render(packet))
            return 0
    sys.stdout.write(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except ContractError as exc:
        sys.stderr.write(json.dumps({"error": {"code": exc.code, "path": exc.path, "message": exc.message}}, ensure_ascii=False) + "\n")
        sys.exit(2)
    except (OSError, UnicodeError, RecursionError, OverflowError, ValueError, TypeError) as exc:
        sys.stderr.write(json.dumps({"error": {"code": "input_or_resource", "path": "$", "message": str(exc)}}) + "\n")
        sys.exit(2)
