"""Versioned planning/selection checks, not proof of real design or composition."""

import copy
import itertools
import json
import subprocess
import sys
import unittest

from support import ROOT, calculator as c, fixture, row


def portfolio():
    return c.loads((ROOT / "assets/example-portfolio.json").read_text(encoding="utf-8"))


def alternatives():
    packet = portfolio()
    planning = packet["planning"]
    planning["mode"] = "alternatives"
    planning["areas"] = planning["areas"][:1]
    for assignment in planning["assignments"]:
        assignment.update(area_ids=["callers"], depends_on=[])
    for relation in planning["relations"]:
        relation["relationship"] = "alternative"
    for field in ("recommendation", "decision"):
        del packet[field]["plan_ids"]
    return packet


def add_plan(packet, plan_id="D"):
    plan = copy.deepcopy(packet["plans"][0])
    plan.update(id=plan_id, strategy_id="synthetic-strategy-" + plan_id)
    packet["plans"].append(plan)
    packet["critique"]["reviewed_plans"].append({"plan_id": plan_id, "plan_revision": 1})
    record = copy.deepcopy(next(r for r in packet["run_record"] if r["role"] == "planner"))
    record.update(context_id="synthetic-context-" + plan_id, call_id="synthetic-call-" + plan_id,
                  strategy_id=plan["strategy_id"])
    packet["run_record"].append(record)
    if "planning" in packet:
        planning = packet["planning"]
        planning["assignments"].append({"plan_id": plan_id, "area_ids": [planning["areas"][0]["id"]], "depends_on": []})
        review = packet["critique"]["design_review"]
        individual = copy.deepcopy(review["plans"][1])
        individual["plan_id"] = plan_id
        review["plans"].append(individual)
        for other in packet["plans"][:-1]:
            relation = copy.deepcopy(planning["relations"][0])
            relation["plan_ids"] = [other["id"], plan_id]
            planning["relations"].append(relation)
            pair = copy.deepcopy(review["pairwise"][0])
            pair["plan_ids"] = [other["id"], plan_id]
            review["pairwise"].append(pair)


class PlanningModeTests(unittest.TestCase):
    def setUp(self):
        self.packet = portfolio()
        self.planning = self.packet["planning"]

    def rejects(self, code=None, packet=None, type_name="decision_packet"):
        with self.assertRaises(c.ContractError) as caught:
            c.validate(self.packet if packet is None else packet, type_name)
        if code:
            self.assertEqual(caught.exception.code, code, caught.exception.message)

    def pick(self, field, ids):
        self.packet[field]["plan_ids"] = ids
        if field == "decision":
            self.packet[field].update(status="selected", answer="I choose these unimplemented plans for planning only.")

    def test_synthetic_three_area_example_validates_with_unknown_costs(self):
        self.assertEqual(len(self.planning["areas"]), 3)
        self.assertEqual(len(self.packet["plans"]), 3)
        c.validate(self.packet)
        for plan in self.packet["plans"]:
            self.assertIsNone(plan["costs"][0]["hours"]["reference"])
            self.assertEqual(row(c.compare(self.packet), plan["id"])["capacity"]["status"], "unknown")
        self.assertIn("not repository inspection or agent execution", self.packet["context"]["evidence"][0]["source"])

    def test_two_plus_p0_cannot_complete_new_packet(self):
        self.packet["plans"].pop()
        self.rejects("plan_count")

    def test_p0_does_not_count_toward_three_change_plans(self):
        self.packet["plans"][-1] = copy.deepcopy(self.packet["baseline"])
        self.rejects("duplicate_id")

    def test_infeasible_attempt_counts_but_render_is_truthful(self):
        self.packet["plans"][0]["status"] = "infeasible"
        c.validate(self.packet)
        rendered = c.render(self.packet)
        self.assertIn("Change proposals: 3 (P0 excluded)", rendered)
        self.assertIn("viable=2, infeasible=1", rendered)
        self.assertIn("excluded=1", rendered)
        self.assertIn("not as viable choices", rendered)

    def test_legacy_two_preserved_and_maximum_three_enforced(self):
        packet = fixture()
        c.validate(packet)
        add_plan(packet, "C")
        c.validate(packet)
        add_plan(packet)
        self.rejects("plan_count", packet)

    def test_four_new_plans_require_all_six_relation_and_design_pairs(self):
        add_plan(self.packet)
        c.validate(self.packet)
        self.assertEqual(len(self.planning["relations"]), 6)
        self.assertEqual(len(self.packet["critique"]["design_review"]["pairwise"]), 6)
        expected = {frozenset(pair) for pair in itertools.combinations("ABCD", 2)}
        self.assertEqual({frozenset(r["plan_ids"]) for r in self.planning["relations"]}, expected)

    def test_fourth_plan_missing_relation_rejected(self):
        add_plan(self.packet)
        self.planning["relations"].pop()
        self.rejects("planning_coverage")

    def test_fourth_plan_missing_design_pair_rejected(self):
        add_plan(self.packet)
        self.packet["critique"]["design_review"]["pairwise"].pop()
        self.rejects("design_coverage")

    def test_new_requires_current_context_version(self):
        self.packet["context"]["schema_version"] = "1.0"
        self.rejects("version")

    def test_new_requires_planning(self):
        del self.packet["planning"]
        self.rejects("required")

    def test_new_requires_design_review(self):
        del self.packet["critique"]["design_review"]
        self.rejects("required")

    def test_unknown_schema_versions_rejected(self):
        for target in (self.packet, self.packet["context"]):
            target["schema_version"] = "1.2"
            self.rejects("enum")
            target["schema_version"] = "1.1"

    def test_legacy_cannot_bypass_minimum_by_adding_planning(self):
        packet = fixture()
        packet["planning"] = self.planning
        self.rejects("version", packet)

    def test_legacy_rejects_new_only_selection_fields_even_if_empty(self):
        packet = fixture()
        for field in ("recommendation", "decision"):
            packet[field]["plan_ids"] = []
            self.rejects("version", packet)
            del packet[field]["plan_ids"]
        c.validate(packet)

    def test_missing_assignment_rejected(self):
        self.planning["assignments"].pop()
        self.rejects("reference")

    def test_extra_unknown_assignment_rejected(self):
        self.planning["assignments"].append({"plan_id": "missing", "area_ids": ["callers"], "depends_on": []})
        self.rejects("reference")

    def test_duplicate_assignment_rejected(self):
        self.planning["assignments"].append(copy.deepcopy(self.planning["assignments"][0]))
        self.rejects("duplicate_id")

    def test_p0_assignment_rejected(self):
        self.planning["assignments"][0]["plan_id"] = "P0"
        self.rejects("reference")

    def test_unknown_area_rejected(self):
        self.planning["assignments"][0]["area_ids"] = ["missing"]
        self.rejects("reference")

    def test_empty_area_assignment_rejected(self):
        self.planning["assignments"][0]["area_ids"] = []
        self.rejects("length")

    def test_duplicate_area_assignment_rejected(self):
        self.planning["assignments"][0]["area_ids"] *= 2
        self.rejects("duplicate_id")

    def test_duplicate_area_id_rejected(self):
        self.planning["areas"].append(copy.deepcopy(self.planning["areas"][0]))
        self.rejects("duplicate_id")

    def test_uncovered_area_rejected(self):
        self.planning["assignments"][1]["area_ids"] = ["callers"]
        self.rejects("planning_coverage")

    def test_one_plan_can_cover_multiple_existing_areas(self):
        self.planning["assignments"][0]["area_ids"].append("reporting")
        c.validate(self.packet)

    def test_missing_relation_rejected(self):
        self.planning["relations"].pop()
        self.rejects("planning_coverage")

    def test_duplicate_and_reversed_relations_rejected(self):
        for reverse in (False, True):
            with self.subTest(reverse=reverse):
                relation = copy.deepcopy(self.planning["relations"][0])
                if reverse:
                    relation["plan_ids"].reverse()
                self.planning["relations"].append(relation)
                self.rejects("duplicate_id")
                self.planning["relations"].pop()

    def test_relation_pair_requires_two_distinct_ids(self):
        self.planning["relations"][0]["plan_ids"] = ["A", "A"]
        self.rejects("duplicate_id")

    def test_relation_pair_rejects_p0_or_unknown(self):
        for plan_id in ("P0", "missing"):
            self.planning["relations"][0]["plan_ids"] = ["A", plan_id]
            self.rejects("reference")

    def test_relation_pair_requires_exactly_two_ids(self):
        for ids in (["A"], ["A", "B", "C"]):
            self.planning["relations"][0]["plan_ids"] = ids
            self.rejects("length")

    def test_relation_evidence_uses_packet_registry(self):
        self.planning["relations"][0]["evidence_ids"] = ["missing"]
        self.rejects("reference")
        # Local planning cannot authenticate the external evidence registry.
        c.validate(self.planning, "planning")

    def test_standalone_planning_cannot_detect_omitted_external_plan(self):
        self.planning["assignments"].pop()
        self.planning["areas"].pop()
        self.planning["relations"] = self.planning["relations"][:1]
        c.validate(self.planning, "planning")
        self.rejects("reference")

    def test_duplicate_relation_evidence_rejected(self):
        self.planning["relations"][0]["evidence_ids"] = ["E1", "E1"]
        self.rejects("duplicate_id")

    def test_forward_prerequisite_order_is_allowed(self):
        self.planning["assignments"].reverse()
        c.validate(self.packet)

    def test_prerequisites_reject_p0_self_unknown_and_duplicates(self):
        for dependencies, code in ((["P0"], "reference"), (["A"], "reference"),
                                   (["missing"], "reference"), (["B", "B"], "duplicate_id")):
            with self.subTest(dependencies=dependencies):
                self.planning["assignments"][0]["depends_on"] = dependencies
                self.rejects(code)

    def test_plan_prerequisites_must_be_dag(self):
        self.planning["assignments"][0]["depends_on"] = ["B"]
        self.planning["assignments"][1]["depends_on"] = ["C"]
        self.rejects("cycle")

    def test_alternatives_mode_three_plans_valid_and_single_choice_preserved(self):
        packet = alternatives()
        packet["recommendation"]["plan_id"] = "A"
        packet["decision"].update(status="selected", plan_id="B", answer="Choose B for planning only.")
        c.validate(packet)
        self.assertEqual(c.compare(packet)["decision"], packet["decision"])

    def test_alternatives_exactly_one_area(self):
        self.planning["mode"] = "alternatives"
        self.rejects("planning_mode")

    def test_alternatives_no_prerequisites(self):
        packet = alternatives()
        packet["planning"]["assignments"][2]["depends_on"] = ["A"]
        self.rejects("planning_mode", packet)

    def test_alternatives_all_relations_must_be_alternative(self):
        packet = alternatives()
        packet["planning"]["relations"][0]["relationship"] = "independent"
        self.rejects("planning_mode", packet)

    def test_alternatives_plan_ids_must_be_absent_or_empty(self):
        packet = alternatives()
        for field in ("recommendation", "decision"):
            packet[field]["plan_ids"] = []
            c.validate(packet)
            packet[field]["plan_ids"] = ["A"]
            self.rejects("selection", packet)
            packet[field]["plan_ids"] = []

    def test_portfolio_requires_two_or_more_areas(self):
        self.planning["areas"] = self.planning["areas"][:1]
        self.rejects("planning_mode")

    def test_empty_areas_rejected(self):
        self.planning["areas"] = []
        self.rejects("length")

    def test_area_scope_and_success_scenarios_nonempty(self):
        area = self.planning["areas"][0]
        for field in ("scope", "success_scenarios"):
            saved = area[field]
            area[field] = []
            self.rejects("length")
            area[field] = saved

    def test_planning_text_whitespace_rejected_recursively(self):
        def leaves(value, path=()):
            if isinstance(value, str):
                yield path
            elif isinstance(value, dict):
                for key, item in value.items():
                    yield from leaves(item, path + (key,))
            elif isinstance(value, list):
                for index, item in enumerate(value):
                    yield from leaves(item, path + (index,))
        for path in leaves(self.planning):
            if path == ("mode",) or path[-1] in ("relationship", "compatibility", "benefit_overlap"):
                continue
            with self.subTest(path=path):
                planning = copy.deepcopy(self.planning)
                target = planning
                for key in path[:-1]:
                    target = target[key]
                target[path[-1]] = " \t\n"
                self.rejects("blank", planning, "planning")

    def test_no_extra_fields_in_any_planning_object(self):
        for value in (self.planning, self.planning["areas"][0], self.planning["assignments"][0], self.planning["relations"][0]):
            value["extra"] = True
            self.rejects("additional_property")
            del value["extra"]

    def test_different_area_ids_do_not_imply_independence_or_no_overlap(self):
        relation = self.planning["relations"][0]
        relation.update(relationship="unknown", compatibility="unknown", benefit_overlap="shared")
        result = c.compare(self.packet)
        self.assertEqual(result["planning"]["relations"][0], relation)
        self.assertIn("Different areas do not imply independence or disjoint benefits", c.render(result))

    def test_relations_and_design_diversity_are_independent(self):
        pair = self.packet["critique"]["design_review"]["pairwise"][0]
        pair.update(status="duplicate", axes=[])
        c.validate(self.packet)
        self.assertEqual(row(c.compare(self.packet))["admissibility"], "admissible")
        self.assertIn("not proof of competing alternatives", c.render(self.packet))
        self.assertIn("does not prove two distinct portfolio contributions", c.render(self.packet))

    def test_portfolio_requires_explicit_plan_ids_in_both_fields(self):
        for field in ("recommendation", "decision"):
            del self.packet[field]["plan_ids"]
            self.rejects("required")
            self.packet[field]["plan_ids"] = []

    def test_portfolio_cannot_mix_single_and_multiple_fields(self):
        for field in ("recommendation", "decision"):
            self.packet[field]["plan_id"] = "A"
            self.rejects("selection")
            self.packet[field]["plan_id"] = None

    def test_multi_pick_closure_allows_compatible_prerequisites(self):
        for field in ("recommendation", "decision"):
            self.pick(field, ["A", "C"])
            c.validate(self.packet)
        self.assertEqual(c.compare(self.packet)["decision"]["plan_ids"], ["A", "C"])

    def test_multi_pick_requires_transitive_prerequisite_closure(self):
        self.planning["assignments"][2]["depends_on"] = ["B"]
        self.planning["assignments"][1]["depends_on"] = ["A"]
        for field in ("recommendation", "decision"):
            for chosen in (["C"], ["B", "C"], ["A", "C"]):
                self.pick(field, chosen)
                self.rejects("prerequisite")
            self.packet[field]["plan_ids"] = []
            if field == "decision":
                self.packet[field].update(status="pending", answer=None)

    def test_conflicting_and_alternative_pairs_cannot_be_chosen_together(self):
        for field in ("recommendation", "decision"):
            for key, value in (("compatibility", "conflicting"), ("relationship", "alternative")):
                relation = self.planning["relations"][1]
                saved = relation[key]
                relation[key] = value
                self.pick(field, ["A", "C"])
                self.rejects("selection")
                relation[key] = saved
            self.packet[field]["plan_ids"] = []

    def test_multi_pick_rejects_unknown_p0_duplicate_and_excluded_ids(self):
        for field in ("recommendation", "decision"):
            for chosen, code in ((["missing"], "reference"), (["P0"], "reference"), (["A", "A"], "duplicate_id")):
                self.pick(field, chosen)
                self.rejects(code)
            self.packet["plans"][0]["status"] = "infeasible"
            self.pick(field, ["A"])
            self.rejects("excluded")
            self.packet["plans"][0]["status"] = "viable"
            self.packet[field]["plan_ids"] = []

    def test_conditional_multi_recommendation_requires_nonblank_conditions(self):
        self.packet["plans"][0]["status"] = "incomplete"
        self.pick("recommendation", ["A"])
        for conditions in ([], ["  "]):
            self.packet["recommendation"]["conditions"] = conditions
            self.rejects("recommendation")
        self.packet["recommendation"]["conditions"] = ["Resolve incomplete design evidence."]
        c.validate(self.packet)

    def test_unknown_compatibility_recommendation_requires_conditions(self):
        self.pick("recommendation", ["A", "B"])
        self.rejects("recommendation")
        self.packet["recommendation"]["conditions"] = ["Review shared caller routing before implementation."]
        c.validate(self.packet)
        self.assertIn("recommendation includes unknown compatibility", c.render(self.packet))

    def test_unknown_compatibility_selection_allowed_but_warned_not_safe(self):
        self.pick("decision", ["A", "B"])
        c.validate(self.packet)
        rendered = c.render(self.packet)
        self.assertIn("decision includes unknown compatibility", rendered)
        self.assertIn("safety is not established", rendered)
        self.assertIn("No implementation or execution approval is implied", rendered)

    def test_pending_deferred_rejected_cannot_pick_portfolio(self):
        for status in ("pending", "deferred", "rejected"):
            self.packet["decision"].update(status=status, answer=None if status == "pending" else "Wait for evidence.", plan_ids=["A"])
            self.rejects("decision")
            self.packet["decision"]["plan_ids"] = []
            c.validate(self.packet)

    def test_selected_requires_nonempty_ids_answer_and_current_revision(self):
        self.packet["decision"].update(status="selected", answer="Choose an unimplemented plan.")
        self.rejects("decision")
        self.packet["decision"].update(plan_ids=["A"], answer=None)
        self.rejects("decision")
        self.packet["decision"].update(answer="Choose A.", context_revision=2)
        self.rejects("stale")

    def test_no_automatic_selection_or_combined_sum_or_assessment_shape_change(self):
        self.pick("recommendation", ["A", "C"])
        result = c.compare(self.packet)
        self.assertEqual(result["decision"]["status"], "pending")
        self.assertEqual(result["decision"]["plan_ids"], [])
        assessment = result["assessment"]
        self.assertEqual(set(assessment), {"formula_version", "horizon_months", "scenario_semantics", "plans",
                                           "sensitivity_horizons", "sensitivity", "reference_break_even"})
        self.assertEqual([p["plan_id"] for p in assessment["plans"]], ["A", "B", "C", "P0"])
        self.assertEqual(assessment["formula_version"], "1.0")
        self.assertIn("No combined estimate", c.render(result))

    def test_portfolio_pairs_not_comparable_but_baseline_stays_standalone(self):
        original = fixture()
        for index in (0, 1):
            for field in ("costs", "monthly_savings_hours", "completion_months"):
                self.packet["plans"][index][field] = copy.deepcopy(original["plans"][index][field])
        self.packet["context"]["horizon_months"] = 12
        result = c.compare(self.packet)
        self.assertEqual(row(result)["capacity"]["values"]["reference"], 68)
        self.assertEqual(row(result, "B")["capacity"]["values"]["reference"], 56)
        for pair in result["assessment"]["reference_break_even"]:
            if "P0" not in pair["plan_ids"]:
                self.assertEqual(pair["status"], "not_comparable")
                self.assertIsNone(pair["horizon_months"])
                self.assertIn("different/nonexclusive objectives", pair["reason"])
            elif pair["plan_ids"] == ["A", "P0"]:
                self.assertEqual(pair["status"], "known")
                self.assertAlmostEqual(pair["horizon_months"], 1 + 64 / 12)
        crossing = next(p for p in c.compare(original)["assessment"]["reference_break_even"] if p["plan_ids"] == ["A", "B"])
        self.assertEqual((crossing["status"], crossing["horizon_months"]), ("known", 13))

    def test_new_alternatives_keep_legacy_crossover_math(self):
        packet = alternatives()
        original = fixture()
        for index in (0, 1):
            for field in ("costs", "monthly_savings_hours", "completion_months"):
                packet["plans"][index][field] = copy.deepcopy(original["plans"][index][field])
        packet["context"]["horizon_months"] = 12
        crossing = next(pair for pair in c.compare(packet)["assessment"]["reference_break_even"] if pair["plan_ids"] == ["A", "B"])
        self.assertEqual((crossing["status"], crossing["horizon_months"]), ("known", 13))

    def test_planning_renders_before_design_and_numeric_with_escaped_raw_fields(self):
        dangerous = "x|y\n`code`<script>*bold*_[link]#\\"
        self.planning["areas"][0]["name"] = dangerous
        self.planning["areas"][0]["objective"] = dangerous
        self.planning["relations"][0]["reason"] = dangerous
        rendered = c.render(self.packet)
        self.assertLess(rendered.index("## Planning mode"), rendered.index("## Design review"))
        self.assertLess(rendered.index("## Design review"), rendered.index("## Comparison"))
        section = rendered.split("## Planning mode", 1)[1].split("## Design review", 1)[0]
        self.assertEqual(section.count(c.escape(dangerous)), 3)
        self.assertIn("depends&#95;on", section)
        self.assertIn("Compatible assertion", section)
        self.assertIn("Unknown compatibility warning", section)
        self.assertNotIn("<script>", rendered)
        self.assertNotIn("{{planning}}", rendered)

    def test_conflict_relations_render_warning_without_forcing_selection(self):
        self.planning["relations"][0]["compatibility"] = "conflicting"
        self.assertIn("Conflicting warning", c.render(self.packet))
        self.assertEqual(c.compare(self.packet)["decision"]["plan_ids"], [])

    def test_multi_ids_raw_rendered_and_source_tokens_not_interpreted(self):
        self.pick("decision", ["A", "C"])
        self.planning["relations"][0]["reason"] = "Literal {{decision}} stays data."
        rendered = c.render(self.packet)
        self.assertIn("Literal {{decision}} stays data.", rendered)
        decision = rendered.split("## Conditional recommendation", 1)[1]
        self.assertIn("plan&#95;ids:", decision)
        self.assertIn("- A", decision)
        self.assertIn("- C", decision)

    def test_planning_ids_and_warning_pairs_are_escaped(self):
        plan_id, evidence_id, area_id = "A|`<x>", "E|`<x>", "area|`<x>"
        self.packet["plans"][0]["id"] = plan_id
        self.planning["areas"][0]["id"] = area_id
        self.planning["assignments"][0].update(plan_id=plan_id, area_ids=[area_id])
        self.planning["assignments"][2]["depends_on"] = [plan_id]
        self.packet["critique"]["reviewed_plans"][1]["plan_id"] = plan_id
        self.packet["critique"]["design_review"]["plans"][1]["plan_id"] = plan_id
        for pairs in (self.planning["relations"], self.packet["critique"]["design_review"]["pairwise"]):
            for pair in pairs:
                pair["plan_ids"] = [plan_id if item == "A" else item for item in pair["plan_ids"]]
        evidence = copy.deepcopy(self.packet["context"]["evidence"][0])
        evidence["id"] = evidence_id
        self.packet["context"]["evidence"].append(evidence)
        self.planning["relations"][0]["evidence_ids"] = [evidence_id]
        self.pick("decision", [plan_id, "B"])
        rendered = c.render(self.packet)
        planning = rendered.split("## Planning mode", 1)[1].split("## Design review", 1)[0]
        for value in (plan_id, evidence_id, area_id):
            self.assertIn(c.escape(value), planning)
            self.assertNotIn(value, rendered)
        self.assertIn("decision includes unknown compatibility: " + c.escape(plan_id + " / B"), planning)

    def test_legacy_count_mode_warning_does_not_modify_packet_or_math(self):
        packet = fixture()
        before = copy.deepcopy(packet)
        assessment = c.compare(packet)["assessment"]
        rendered = c.render(packet)
        self.assertIn("Legacy 1.0 count/mode warning", rendered)
        self.assertIn("2 change proposals (P0 excluded)", rendered)
        self.assertIn("not upgraded to the current minimum of three", rendered)
        self.assertEqual(packet, before)
        self.assertEqual(c.compare(c.loads(json.dumps(c.compare(packet))))["assessment"], assessment)
        self.assertNotIn("planning", c.compare(packet))
        self.assertEqual(assessment["formula_version"], "1.0")

    def test_new_roundtrip_is_deterministic_and_source_unchanged(self):
        before = copy.deepcopy(self.packet)
        compared = c.compare(self.packet)
        restored = c.loads(json.dumps(compared))
        self.assertEqual(c.compare(restored), compared)
        self.assertEqual(c.render(restored), c.render(self.packet))
        self.assertEqual(self.packet, before)
        self.assertEqual(compared["schema_version"], "1.1")

    def test_cli_planning_describe_validate_and_new_packet_roundtrip(self):
        command = [sys.executable, "-B", str(ROOT / "scripts/compare.py")]
        description = subprocess.run(command + ["describe", "--type", "planning"], input="not-json", text=True, capture_output=True, check=False)
        self.assertEqual(description.returncode, 0, description.stderr)
        schema = c.loads(description.stdout)
        c.audit_schema(schema, schema)
        c.schema_validate(self.planning, schema, schema)
        c.validate(self.planning, "planning")
        compared = subprocess.run(command + ["compare"], input=json.dumps(self.packet), text=True, capture_output=True, check=False)
        self.assertEqual(compared.returncode, 0, compared.stderr)
        validation = subprocess.run(command + ["validate", "--type", "decision_packet"], input=compared.stdout, text=True, capture_output=True, check=False)
        self.assertEqual(validation.returncode, 0, validation.stderr)
        self.assertEqual(c.loads(validation.stdout)["schema_version"], "1.1")
        legacy = subprocess.run(command + ["validate", "--type", "decision_packet"], input=json.dumps(fixture()), text=True, capture_output=True, check=False)
        self.assertEqual(legacy.returncode, 0, legacy.stderr)
        self.assertEqual(c.loads(legacy.stdout)["schema_version"], "1.0")
        rendered = subprocess.run(command + ["render"], input=compared.stdout, text=True, capture_output=True, check=False)
        self.assertEqual(rendered.returncode, 0, rendered.stderr)
        self.assertIn("Mode: portfolio", rendered.stdout)


if __name__ == "__main__":
    unittest.main()
