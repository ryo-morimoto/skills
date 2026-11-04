"""Optional design review is structural planning evidence, never execution proof."""

import copy
import itertools
import json
import subprocess
import sys
import unittest

from support import ROOT, calculator as c, fixture, row, unknown


CRITERIA = ("goal_fit", "responsibility", "dependencies", "contract", "migration", "verification_recovery")


def plan_review(plan_id):
    return {"plan_id": plan_id, "status": "plausible", "checks": [
        {"criterion": criterion, "status": "pass", "reason": "Synthetic planning rationale, not executed tests.",
         "evidence_ids": ["E1"]} for criterion in CRITERIA], "unresolved": []}


def pair_review(left, right):
    return {"plan_ids": [left, right], "status": "distinct", "axes": [
        {"axis": "responsibility", "difference": "Synthetic boundary ownership differs, not merely names or estimates.",
         "evidence_ids": ["E1"]}], "reason": "Synthetic structural distinction, not a semantic truth guarantee."}


class DesignReviewTests(unittest.TestCase):
    def setUp(self):
        self.packet = fixture()
        self.review = {"version": "1.0", "pairwise": [pair_review("A", "B")],
                       "plans": [plan_review(plan_id) for plan_id in ("P0", "A", "B")]}
        self.packet["critique"]["design_review"] = self.review
        self.pair = self.review["pairwise"][0]
        self.plan = self.review["plans"][1]

    def rejects(self, code=None, standalone=False):
        with self.assertRaises(c.ContractError) as caught:
            if standalone:
                c.validate(self.packet["critique"], "critique_result")
            else:
                c.validate(self.packet)
        if code:
            self.assertEqual(caught.exception.code, code)

    def verdict(self, verdict, check_status):
        self.plan["status"] = verdict
        self.plan["checks"][0]["status"] = check_status

    def third_plan(self):
        plan = copy.deepcopy(self.packet["plans"][0])
        plan.update(id="C", strategy_id="synthetic-third")
        self.packet["plans"].append(plan)
        self.packet["critique"]["reviewed_plans"].append({"plan_id": "C", "plan_revision": 1})
        record = copy.deepcopy(self.packet["run_record"][0])
        record.update(context_id="synthetic-C", call_id="synthetic-call-C", strategy_id="synthetic-third")
        self.packet["run_record"].append(record)
        self.review["plans"].append(plan_review("C"))
        self.review["pairwise"] = [pair_review(*pair) for pair in itertools.combinations(("A", "B", "C"), 2)]

    def test_two_change_plans_require_one_pair_not_baseline_pairs(self):
        c.validate(self.packet)
        c.validate(self.packet["critique"], "critique_result")
        self.assertEqual(len(self.review["pairwise"]), 1)

    def test_three_change_plans_require_all_three_pairs(self):
        self.third_plan()
        c.validate(self.packet)
        c.validate(self.packet["critique"], "critique_result")
        self.assertEqual(len(self.review["pairwise"]), 3)

    def test_missing_only_pair_rejected_packet_and_standalone(self):
        self.review["pairwise"] = []
        self.rejects("design_coverage")
        self.rejects("design_coverage", standalone=True)

    def test_missing_third_plan_pair_rejected_packet_and_standalone(self):
        self.third_plan()
        self.review["pairwise"].pop()
        self.rejects("design_coverage")
        self.rejects("design_coverage", standalone=True)

    def test_missing_baseline_review_rejected_packet_and_standalone(self):
        self.review["plans"].pop(0)
        self.rejects("reference")
        self.rejects("reference", standalone=True)

    def test_missing_change_plan_review_rejected_packet_and_standalone(self):
        self.review["plans"].pop()
        self.rejects("reference")
        self.rejects("reference", standalone=True)

    def test_duplicate_plan_review_rejected(self):
        self.review["plans"].append(copy.deepcopy(self.plan))
        self.rejects("duplicate_id")
        self.rejects("duplicate_id", standalone=True)

    def test_duplicate_pair_rejected(self):
        self.review["pairwise"].append(copy.deepcopy(self.pair))
        self.rejects("duplicate_id")
        self.rejects("duplicate_id", standalone=True)

    def test_reversed_pair_rejected(self):
        pair = copy.deepcopy(self.pair)
        pair["plan_ids"].reverse()
        self.review["pairwise"].append(pair)
        self.rejects("duplicate_id")
        self.rejects("duplicate_id", standalone=True)

    def test_pair_requires_two_unique_ids(self):
        self.pair["plan_ids"] = ["A", "A"]
        self.rejects("duplicate_id")

    def test_pair_requires_exactly_two_ids(self):
        for ids in (["A"], ["A", "B", "P0"]):
            with self.subTest(ids=ids):
                self.pair["plan_ids"] = ids
                self.rejects("length")

    def test_pair_cannot_include_baseline(self):
        self.pair["plan_ids"] = ["P0", "A"]
        self.rejects("reference")
        self.rejects("reference", standalone=True)

    def test_unknown_pair_plan_id_rejected(self):
        self.pair["plan_ids"] = ["A", "missing"]
        self.rejects("reference")
        self.rejects("reference", standalone=True)

    def test_unknown_review_plan_id_rejected(self):
        self.plan["plan_id"] = "missing"
        self.rejects("reference")
        self.rejects("reference", standalone=True)

    def test_standalone_uses_reviewed_plans_not_design_plans_as_authority(self):
        self.packet["critique"]["reviewed_plans"].pop()
        self.rejects("reference", standalone=True)

    def test_standalone_with_design_requires_baseline_among_reviewed_plans(self):
        self.packet["critique"]["reviewed_plans"].pop(0)
        self.review["plans"].pop(0)
        self.rejects("reference", standalone=True)

    def test_unknown_axis_evidence_id_rejected_in_packet(self):
        self.pair["axes"][0]["evidence_ids"] = ["missing"]
        self.rejects("reference")

    def test_unknown_check_evidence_id_rejected_in_packet(self):
        self.plan["checks"][0]["evidence_ids"] = ["missing"]
        self.rejects("reference")

    def test_duplicate_evidence_references_rejected_also_standalone(self):
        for value in (self.pair["axes"][0], self.plan["checks"][0]):
            with self.subTest(value=value):
                value["evidence_ids"] = ["E1", "E1"]
                self.rejects("duplicate_id")
                self.rejects("duplicate_id", standalone=True)
                value["evidence_ids"] = ["E1"]

    def test_stale_reviewed_plan_still_rejected_with_design_review(self):
        self.packet["plans"][0]["plan_revision"] = 2
        self.rejects("stale")

    def test_six_checks_required_for_every_plan_including_baseline(self):
        for plan in self.review["plans"]:
            with self.subTest(plan=plan["plan_id"]):
                check = plan["checks"].pop()
                self.rejects("length")
                self.rejects("length", standalone=True)
                plan["checks"].append(check)

    def test_duplicate_criterion_cannot_replace_missing_criterion(self):
        self.plan["checks"][-1] = copy.deepcopy(self.plan["checks"][0])
        self.rejects("duplicate_id")

    def test_seventh_check_rejected(self):
        self.plan["checks"].append(copy.deepcopy(self.plan["checks"][0]))
        self.rejects("length")

    def test_plausible_requires_all_pass(self):
        for status in ("conditional", "unknown", "fail"):
            with self.subTest(status=status):
                self.verdict("plausible", status)
                self.rejects("design_verdict")

    def test_invalid_requires_at_least_one_fail(self):
        for status in ("pass", "conditional", "unknown"):
            with self.subTest(status=status):
                self.verdict("invalid", status)
                self.rejects("design_verdict")

    def test_any_fail_requires_invalid(self):
        for verdict in ("plausible", "conditional", "unknown"):
            with self.subTest(verdict=verdict):
                self.verdict(verdict, "fail")
                self.rejects("design_verdict")
                self.rejects("design_verdict", standalone=True)
        self.verdict("invalid", "fail")
        c.validate(self.packet)

    def test_conditional_requires_conditional_or_unknown_check(self):
        self.verdict("conditional", "pass")
        self.rejects("design_verdict")
        for status in ("conditional", "unknown"):
            with self.subTest(status=status):
                self.verdict("conditional", status)
                c.validate(self.packet)

    def test_unknown_requires_unknown_check(self):
        for status in ("pass", "conditional"):
            with self.subTest(status=status):
                self.verdict("unknown", status)
                self.rejects("design_verdict")
        self.verdict("unknown", "unknown")
        c.validate(self.packet)

    def test_invalid_excluded_even_with_pass_gates_and_no_blocking_findings(self):
        self.verdict("invalid", "fail")
        self.packet["critique"]["findings"] = []
        result = c.compare(self.packet)
        self.assertEqual(row(result)["admissibility"], "excluded")
        self.assertEqual(len(result["plans"]), 2)

    def test_invalid_cannot_be_recommended(self):
        self.verdict("invalid", "fail")
        self.packet["recommendation"]["plan_id"] = "A"
        self.rejects("excluded")

    def test_invalid_cannot_be_selected(self):
        self.verdict("invalid", "fail")
        self.packet["decision"].update(status="selected", plan_id="A", answer="Choose A")
        self.rejects("excluded")

    def test_conditional_and_unknown_propagate_without_changing_capacity(self):
        before = row(c.compare(self.packet))["capacity"]
        for status in ("conditional", "unknown"):
            with self.subTest(status=status):
                self.verdict(status, status)
                result = row(c.compare(self.packet))
                self.assertEqual(result["admissibility"], "conditional")
                self.assertEqual(result["capacity"], before)

    def test_design_conditional_recommendation_needs_explicit_conditions(self):
        self.verdict("conditional", "conditional")
        self.packet["recommendation"].update(plan_id="A", conditions=[])
        self.rejects("recommendation")
        self.packet["recommendation"]["conditions"] = ["Resolve the design condition."]
        c.validate(self.packet)

    def test_duplicate_pair_is_not_individual_invalidity_or_automatic_exclusion(self):
        self.pair.update(status="duplicate", axes=[])
        self.packet["recommendation"]["plan_id"] = "A"
        self.packet["decision"].update(status="selected", plan_id="B", answer="Choose B")
        result = c.compare(self.packet)
        self.assertEqual([row(result, plan_id)["admissibility"] for plan_id in ("A", "B")], ["admissible", "admissible"])
        self.assertEqual(len(result["plans"]), 2)
        rendered = c.render(result)
        self.assertIn("does not count as two meaningful alternatives", rendered)
        self.assertIn("neither plan is automatically excluded", rendered)

    def test_distinct_and_overlapping_need_axes(self):
        self.pair["axes"] = []
        for status in ("distinct", "overlapping"):
            with self.subTest(status=status):
                self.pair["status"] = status
                self.rejects("design_axis")

    def test_difference_axis_cannot_be_whitespace(self):
        self.pair["axes"][0]["difference"] = " \n\t"
        self.rejects("design_axis")

    def test_duplicate_and_unknown_can_have_empty_axes(self):
        self.pair["axes"] = []
        for status in ("duplicate", "unknown"):
            with self.subTest(status=status):
                self.pair["status"] = status
                c.validate(self.packet)
                c.validate(self.packet["critique"], "critique_result")

    def test_unknown_diversity_does_not_change_individual_admissibility(self):
        self.pair.update(status="unknown", axes=[])
        self.assertEqual(row(c.compare(self.packet))["admissibility"], "admissible")
        self.assertIn("meaningful differences are not established", c.render(self.packet))

    def test_unmeasured_cost_does_not_invalidate_plausible_architecture(self):
        self.packet["plans"][0]["costs"][0]["hours"] = unknown(self.packet["plans"][0]["costs"][0]["hours"])
        result = row(c.compare(self.packet))
        self.assertEqual(result["admissibility"], "admissible")
        self.assertEqual(result["capacity"]["status"], "unknown")

    def test_baseline_no_improvement_is_not_automatically_invalid(self):
        baseline = row(c.compare(self.packet), "P0")
        self.assertEqual(baseline["capacity"]["values"]["reference"], 0)
        self.assertEqual(baseline["admissibility"], "admissible")

    def test_render_design_tables_precede_numeric_comparison_and_keep_raw_critique(self):
        self.plan["unresolved"] = ["Resolve synthetic condition before implementation."]
        rendered = c.render(self.packet)
        design = rendered.split("## Design review", 1)[1].split("## Comparison", 1)[0]
        for text in ("| Change-plan pair |", "| Plan | Planning validity |", "A / B", "distinct",
                     "responsibility", self.pair["reason"], self.pair["axes"][0]["difference"],
                     "Synthetic planning rationale", "Resolve synthetic condition", "not executed test success", "P0"):
            with self.subTest(text=text):
                self.assertIn(text, design)
        self.assertIn("design&#95;review:", rendered.split("## Independent critique", 1)[1])
        self.assertNotIn("{{design}}", rendered)

    def test_design_render_escapes_all_new_text_fields(self):
        dangerous = "x|y\n`code`<script>*bold*_[link]#\\"
        self.pair["reason"] = dangerous
        self.pair["axes"][0]["difference"] = dangerous
        self.plan["checks"][0]["reason"] = dangerous
        self.plan["unresolved"] = [dangerous]
        rendered = c.render(self.packet)
        escaped = "x&#124;y&#10;&#96;code&#96;&lt;script&gt;&#42;bold&#42;&#95;&#91;link&#93;&#35;&#92;"
        design = rendered.split("## Design review", 1)[1].split("## Comparison", 1)[0]
        self.assertEqual(design.count(escaped), 4)
        self.assertNotIn("<script>", rendered)

    def test_design_render_escapes_plan_and_evidence_ids(self):
        plan_id, evidence_id = "A|`<x>", "E|`<x>"
        self.packet["plans"][0]["id"] = plan_id
        self.packet["critique"]["reviewed_plans"][1]["plan_id"] = plan_id
        self.plan["plan_id"] = plan_id
        self.pair["plan_ids"][0] = plan_id
        evidence = copy.deepcopy(self.packet["context"]["evidence"][0])
        evidence["id"] = evidence_id
        self.packet["context"]["evidence"].append(evidence)
        self.pair["axes"][0]["evidence_ids"] = [evidence_id]
        self.plan["checks"][0]["evidence_ids"] = [evidence_id]
        design = c.render(self.packet).split("## Design review", 1)[1].split("## Comparison", 1)[0]
        self.assertIn("A&#124;&#96;&lt;x&gt;", design)
        self.assertIn("E&#124;&#96;&lt;x&gt;", design)

    def test_render_does_not_interpret_design_source_template_tokens(self):
        self.pair["reason"] = "Literal {{decision}} is data."
        self.assertIn("Literal {{decision}} is data.", c.render(self.packet))

    def test_legacy_warning_does_not_change_raw_results_or_admissibility(self):
        packet = fixture()
        before = copy.deepcopy(packet)
        rendered = c.render(packet)
        self.assertIn("Design evaluation not supplied", rendered)
        self.assertIn("not retroactively validated", rendered)
        self.assertEqual(packet, before)
        self.assertNotIn("design_review", c.compare(packet)["critique"])
        self.assertEqual(row(c.compare(packet))["admissibility"], "admissible")

    def test_legacy_computed_packet_round_trips_without_assessment_shape_change(self):
        legacy = c.compare(fixture(), [12, 14])
        self.assertNotIn("design_review", legacy["critique"])
        serialized = json.dumps(legacy)
        restored = c.loads(serialized)
        c.verify_assessment(restored)
        self.assertEqual(c.canonical(c.compare(restored, [12, 14])), c.canonical(legacy))
        self.assertEqual(c.render(restored), c.render(c.compare(fixture(), [12, 14])))
        current = c.compare(self.packet, [12, 14])
        self.assertEqual(current["assessment"], legacy["assessment"])
        self.assertEqual(current["assessment"]["formula_version"], "1.0")

    def test_archived_computed_packet_still_verifies_without_artifact_writes(self):
        path = ROOT / "evals/results/product-iteration-1/local-boundary/with_skill/outputs/decision.json"
        if not path.is_file():
            self.skipTest("Optional archived local evaluation is not packaged")
        original = path.read_bytes()
        packet = c.loads(original.decode("utf-8"))
        self.assertIn("assessment", packet)
        self.assertNotIn("design_review", packet["critique"])
        c.validate(packet)
        c.verify_assessment(packet)
        self.assertIn("Design evaluation not supplied", c.render(packet))
        self.assertEqual(c.compare(packet, packet["assessment"]["sensitivity_horizons"]), packet)
        self.assertEqual(path.read_bytes(), original)

    def test_new_design_computed_round_trip_and_source_immutability(self):
        before = copy.deepcopy(self.packet)
        result = c.compare(self.packet)
        self.assertEqual(c.compare(result), result)
        self.assertEqual(c.render(result), c.render(self.packet))
        self.assertEqual(self.packet, before)
        self.assertEqual(result["critique"]["design_review"], self.review)

    def test_new_design_status_makes_old_assessment_stale(self):
        result = c.compare(self.packet)
        result["critique"]["design_review"]["plans"][1]["status"] = "invalid"
        result["critique"]["design_review"]["plans"][1]["checks"][0]["status"] = "fail"
        with self.assertRaises(c.ContractError) as caught:
            c.render(result)
        self.assertEqual(caught.exception.code, "assessment")

    def test_describe_design_review_transitive_and_cli_supported(self):
        subset = c.describe("design_review", c.load_schema())
        c.audit_schema(subset, subset)
        c.schema_validate(self.review, subset, subset)
        c.validate(self.review, "design_review")
        result = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/compare.py"),
                                 "describe", "--type", "design_review"],
                                input="not-json", text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), subset)

    def test_no_numeric_diversity_score_or_extra_design_fields(self):
        for value in (self.review, self.pair, self.plan):
            with self.subTest(value=value):
                value["score"] = 90
                self.rejects("additional_property")
                del value["score"]

    def test_unknown_axis_and_criterion_rejected(self):
        self.pair["axes"][0]["axis"] = "cost_score"
        self.rejects("enum")
        self.pair["axes"][0]["axis"] = "responsibility"
        self.plan["checks"][0]["criterion"] = "executed_test_success"
        self.rejects("enum")

    def test_example_standalone_critique_is_synthetic_and_packet_compatible(self):
        critique = c.loads((ROOT / "assets/example-design-review.json").read_text(encoding="utf-8"))
        c.validate(critique, "critique_result")
        self.assertIn("synthetic", critique["disagreements"][0])
        packet = fixture()
        packet["critique"] = critique
        result = c.compare(packet)
        self.assertEqual(row(result, "B")["admissibility"], "conditional")
        self.assertIn("| Change-plan pair |", c.render(result))


if __name__ == "__main__":
    unittest.main()
