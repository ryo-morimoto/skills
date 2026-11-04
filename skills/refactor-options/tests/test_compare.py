import copy
import json
import subprocess
import sys
import unittest

from support import ROOT, calculator as c, fixture, row, unknown


class ComparisonTests(unittest.TestCase):
    def setUp(self):
        self.packet = fixture()
        self.plan = self.packet["plans"][0]

    def test_reference_arithmetic_h12(self):
        result = c.compare(self.packet)
        self.assertEqual(row(result)["capacity"]["values"]["reference"], 68)
        self.assertEqual(row(result, "B")["capacity"]["values"]["reference"], 56)

    def test_scenario_arithmetic_is_not_probability(self):
        result = c.compare(self.packet)
        self.assertEqual(row(result)["capacity"]["values"], {"low": 8, "reference": 68, "high": 128})
        self.assertEqual(row(result, "B")["capacity"]["values"], {"low": -96, "reference": 56, "high": 168})

    def test_h14_arithmetic(self):
        self.packet["context"]["horizon_months"] = 14
        result = c.compare(self.packet)
        self.assertEqual(row(result)["capacity"]["values"]["reference"], 92)
        self.assertEqual(row(result, "B")["capacity"]["values"]["reference"], 104)

    def test_alternative_cost140_gives_b76(self):
        self.packet["plans"][1]["costs"][0]["hours"]["reference"] = 140
        self.assertEqual(row(c.compare(self.packet), "B")["capacity"]["values"]["reference"], 76)

    def test_reference_break_even13(self):
        assessment = c.compare(self.packet)["assessment"]
        crossing = next(item for item in assessment["reference_break_even"] if item["plan_ids"] == ["A", "B"])
        self.assertEqual(crossing["status"], "known")
        self.assertEqual(crossing["horizon_months"], 13)

    def test_reference_tie_h13(self):
        self.packet["context"]["horizon_months"] = 13
        result = c.compare(self.packet)
        self.assertEqual(row(result)["capacity"]["values"]["reference"], 80)
        self.assertEqual(row(result, "B")["capacity"]["values"]["reference"], 80)

    def test_break_even_before_completion_is_outside_domain(self):
        hours = self.plan["costs"][0]["hours"]
        hours.update(low=0, reference=0, high=0)
        self.plan["completion_months"].update(low=10, reference=10, high=10)
        crossing = next(item for item in c.compare(self.packet)["assessment"]["reference_break_even"] if item["plan_ids"] == ["A", "P0"])
        self.assertEqual(crossing["horizon_months"], 10)
        self.plan["monthly_savings_hours"].update(low=16, reference=24, high=32)
        crossing = next(item for item in c.compare(self.packet)["assessment"]["reference_break_even"] if item["plan_ids"] == ["A", "B"])
        self.assertEqual(crossing["status"], "no_crossing")

    def test_negative_intersection_not_claimed_as_break_even(self):
        self.plan["monthly_savings_hours"].update(low=24, reference=48, high=64)
        crossing = next(item for item in c.compare(self.packet)["assessment"]["reference_break_even"] if item["plan_ids"] == ["A", "B"])
        self.assertEqual(crossing["status"], "outside_domain")
        self.assertIsNone(crossing["horizon_months"])

    def test_completion_later_than_horizon_has_no_benefit(self):
        self.plan["completion_months"].update(low=20, reference=20, high=20)
        self.assertEqual(row(c.compare(self.packet))["capacity"]["values"], {"low": -80, "reference": -64, "high": -48})

    def test_horizon_zero_is_valid(self):
        self.packet["context"]["horizon_months"] = 0
        result = c.compare(self.packet)
        self.assertEqual(row(result)["capacity"]["values"]["reference"], -64)
        self.assertEqual(result["assessment"]["sensitivity_horizons"], [0, 1])

    def test_unknown_horizon_stays_unknown(self):
        self.packet["context"]["horizon_months"] = None
        result = c.compare(self.packet)
        self.assertIsNone(row(result)["capacity"]["values"])
        self.assertEqual(result["assessment"]["sensitivity"], [])

    def test_unknown_horizon_can_have_explicit_sensitivity(self):
        self.packet["context"]["horizon_months"] = None
        result = c.compare(self.packet, [12, 14])
        self.assertEqual(row(result)["capacity"]["status"], "unknown")
        self.assertEqual(result["assessment"]["sensitivity"][0]["plans"][0]["capacity"]["values"]["reference"], 68)

    def test_unknown_savings_never_becomes_zero(self):
        self.plan["monthly_savings_hours"] = unknown(self.plan["monthly_savings_hours"])
        result = row(c.compare(self.packet))
        self.assertEqual(result["capacity"]["status"], "unknown")
        self.assertIsNone(result["capacity"]["values"])
        self.assertIn("monthly_savings_hours", result["capacity"]["missing"])

    def test_unknown_completion_never_becomes_zero(self):
        self.plan["completion_months"] = unknown(self.plan["completion_months"])
        self.assertEqual(row(c.compare(self.packet))["capacity"]["status"], "unknown")

    def test_unknown_cost_never_becomes_zero(self):
        self.plan["costs"][0]["hours"] = unknown(self.plan["costs"][0]["hours"])
        result = row(c.compare(self.packet))
        self.assertEqual(result["cost"]["status"], "incomplete")
        self.assertIsNone(result["cost"]["total"])
        self.assertIsNone(result["capacity"]["values"])

    def test_partial_cost_retains_known_subtotal_not_total(self):
        self.plan["costs"].append({"id": "missing", "label": "Unestimated migration work", "hours": unknown(self.plan["costs"][0]["hours"])})
        result = row(c.compare(self.packet))
        self.assertEqual(result["cost"]["known_subtotal"], {"low": 48, "reference": 64, "high": 80})
        self.assertEqual(result["cost"]["unknown_component_ids"], ["missing"])
        self.assertIsNone(result["cost"]["total"])
        self.assertIsNone(result["capacity"]["values"])

    def test_empty_costs_are_incomplete_not_zero_total(self):
        self.plan["costs"] = []
        result = row(c.compare(self.packet))
        self.assertTrue(result["cost"]["empty_components"])
        self.assertEqual(result["cost"]["known_subtotal"]["reference"], 0)
        self.assertIsNone(result["cost"]["total"])
        self.assertIsNone(result["capacity"]["values"])

    def test_cost_components_sum_scenarios(self):
        cost = copy.deepcopy(self.plan["costs"][0])
        cost["id"] = "extra"
        cost["hours"].update(low=1, reference=2, high=3)
        self.plan["costs"].append(cost)
        self.assertEqual(row(c.compare(self.packet))["cost"]["total"], {"low": 49, "reference": 66, "high": 83})

    def test_sensitivity_default_and_explicit_horizons(self):
        self.assertEqual(c.compare(self.packet)["assessment"]["sensitivity_horizons"], [11, 12, 13])
        result = c.compare(self.packet, [14, 12, 14])
        self.assertEqual(result["assessment"]["sensitivity_horizons"], [12, 14])
        self.assertEqual(row(result)["capacity"]["values"]["reference"], 68)

    def test_sensitivity_invalid_horizon_rejected(self):
        for horizon in (-1, float("nan"), float("inf"), True, "12"):
            with self.subTest(horizon=horizon), self.assertRaises(c.ContractError):
                c.compare(self.packet, [horizon])

    def test_gate_fail_excluded_without_discarding(self):
        self.plan["gates"][0]["status"] = "fail"
        result = c.compare(self.packet)
        self.assertEqual(row(result)["admissibility"], "excluded")
        self.assertEqual(len(result["plans"]), 2)

    def test_gate_unknown_conditional(self):
        self.plan["gates"][0]["status"] = "unknown"
        self.assertEqual(row(c.compare(self.packet))["admissibility"], "conditional")

    def test_missing_gate_conditional(self):
        self.plan["gates"] = []
        result = row(c.compare(self.packet))
        self.assertEqual(result["admissibility"], "conditional")
        self.assertEqual(result["missing_gate_ids"], ["G1"])

    def test_infeasible_excluded_and_incomplete_conditional(self):
        self.plan["status"] = "infeasible"
        self.assertEqual(row(c.compare(self.packet))["admissibility"], "excluded")
        self.plan["status"] = "incomplete"
        self.assertEqual(row(c.compare(self.packet))["admissibility"], "conditional")

    def test_blocking_and_major_critique_affect_admissibility(self):
        finding = self.packet["critique"]["findings"][0]
        finding.update(plan_id="A", severity="blocking")
        self.assertEqual(row(c.compare(self.packet))["admissibility"], "excluded")
        finding["severity"] = "major"
        self.assertEqual(row(c.compare(self.packet))["admissibility"], "conditional")

    def test_risk_severity_is_maximum_only_not_average_or_product(self):
        risk = copy.deepcopy(self.plan["risks"][0])
        risk.update(id="other-risk", residual_severity=5)
        self.plan["risks"].append(risk)
        result = row(c.compare(self.packet))
        self.assertEqual(result["maximum_identified_residual_severity"], 5)
        self.assertEqual(result["maximum_severity_risk_ids"], ["other-risk"])
        self.assertNotIn("risk_score", result)

    def test_unknown_risk_retained_not_safe_zero(self):
        result = row(c.compare(self.packet), "P0")
        self.assertIsNone(result["maximum_identified_residual_severity"])
        self.assertEqual(result["unknown_severity_risk_ids"], ["R0"])

    def test_no_implicit_recommendation_or_human_selection(self):
        self.packet["recommendation"].update(plan_id="A", reason="User priorities would favor early gains.")
        result = c.compare(self.packet)
        self.assertEqual(result["recommendation"], self.packet["recommendation"])
        self.assertEqual(result["decision"]["status"], "pending")
        self.assertIsNone(result["decision"]["plan_id"])

    def test_source_dict_not_mutated(self):
        original = copy.deepcopy(self.packet)
        c.compare(self.packet)
        c.render(self.packet)
        self.assertEqual(original, self.packet)

    def test_order_invariance_of_computed_data(self):
        before = c.compare(self.packet)["assessment"]
        self.packet["plans"].reverse()
        self.packet["run_record"].reverse()
        self.packet["critique"]["reviewed_plans"].reverse()
        self.assertEqual(c.compare(self.packet)["assessment"], before)

    def test_cost_component_order_invariant(self):
        for number in range(5):
            item = copy.deepcopy(self.plan["costs"][0])
            item["id"] = "extra-" + str(number)
            item["hours"].update(low=0.1, reference=0.2, high=0.3)
            self.plan["costs"].append(item)
        before = c.compare(self.packet)["assessment"]
        self.plan["costs"].reverse()
        self.assertEqual(c.compare(self.packet)["assessment"], before)

    def test_baseline_retained_as_delta_not_absolute_maintenance(self):
        result = c.compare(self.packet)
        self.assertEqual(result["baseline"], self.packet["baseline"])
        self.assertEqual(row(result, "P0")["capacity"]["values"]["reference"], 0)
        self.assertTrue(result["baseline"]["risks"])
        self.assertIn("maintenance", result["baseline"]["remaining_debt"][0])

    def test_compare_deterministic_and_idempotent(self):
        first = c.compare(self.packet)
        self.assertEqual(c.canonical(c.compare(first)), c.canonical(first))
        self.assertEqual(c.canonical(c.compare(self.packet)), c.canonical(first))

    def test_render_accepts_raw_and_computed_equally(self):
        self.assertEqual(c.render(self.packet), c.render(c.compare(self.packet)))

    def test_render_rejects_tampered_computed_data(self):
        result = c.compare(self.packet)
        row(result)["capacity"]["values"]["reference"] = 999
        with self.assertRaises(c.ContractError) as caught:
            c.render(result)
        self.assertEqual(caught.exception.code, "assessment")

    def test_compare_rejects_stale_computed_data(self):
        result = c.compare(self.packet)
        result["context"]["horizon_months"] = 14
        with self.assertRaises(c.ContractError):
            c.compare(result)

    def test_render_rejects_tampered_extra_computed_fields(self):
        result = c.compare(self.packet)
        result["assessment"]["recommendation"] = "B"
        with self.assertRaises(c.ContractError):
            c.render(result)

    def test_render_escapes_pipes_newlines_backticks_and_html(self):
        self.plan["caller_example"] = "x|y\n`danger`<script>"
        rendered = c.render(self.packet)
        self.assertIn("x&#124;y&#10;&#96;danger&#96;&lt;script&gt;", rendered)
        self.assertNotIn("<script>", rendered)

    def test_render_preserves_steps_contracts_recovery_unknowns_and_decision(self):
        rendered = c.render(self.packet)
        for text in ("Specify the existing caller contract.", "Every caller retains", "Restore callers to original entry point", "Unknown; no measured frequency.", "pending", "unimplemented", "not proof", "Recurring maintenance", "synthetic-call-A"):
            with self.subTest(text=text):
                self.assertIn(text, rendered)

    def test_render_uses_bundled_static_structure(self):
        rendered = c.render(self.packet)
        self.assertIn("## Full plans, contracts, migration and recovery", rendered)
        self.assertNotIn("{{plans}}", rendered)

    def test_render_does_not_substitute_source_template_tokens(self):
        self.plan["strategy"] = "Literal {{decision}} is not a directive."
        self.assertIn("Literal {{decision}} is not a directive.", c.render(self.packet))

    def test_cli_computed_round_trip_and_tampering(self):
        command = [sys.executable, "-B", str(ROOT / "scripts" / "compare.py")]
        compared = subprocess.run(command + ["compare", "--horizons", "12", "14"], input=json.dumps(self.packet), capture_output=True, text=True, check=False)
        self.assertEqual(compared.returncode, 0, compared.stderr)
        packet = json.loads(compared.stdout)
        self.assertEqual(packet["assessment"]["sensitivity_horizons"], [12.0, 14.0])
        for suffix in (["render"], ["validate", "--type", "decision_packet"]):
            result = subprocess.run(command + suffix, input=compared.stdout, capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0, result.stderr)
        row(packet)["cost"]["total"]["reference"] = 0
        rejected = subprocess.run(command + ["render"], input=json.dumps(packet), capture_output=True, text=True, check=False)
        self.assertEqual(rejected.returncode, 2)
        self.assertEqual(json.loads(rejected.stderr)["error"]["code"], "assessment")
        self.assertNotIn("Traceback", rejected.stderr)


if __name__ == "__main__":
    unittest.main()
