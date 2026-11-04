import copy
import json
import subprocess
import sys
import unittest

from support import ROOT, calculator as c, fixture, unknown


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.packet = fixture()
        self.plan = self.packet["plans"][0]

    def rejects(self, code=None):
        with self.assertRaises(c.ContractError) as caught:
            c.validate(self.packet)
        if code:
            self.assertEqual(caught.exception.code, code)

    def cli(self, *args, text=None):
        return subprocess.run([sys.executable, "-B", str(ROOT / "scripts" / "compare.py"), *args],
                              input=json.dumps(self.packet) if text is None else text,
                              capture_output=True, text=True, check=False)

    def test_example_validates(self):
        self.assertIs(c.validate(self.packet), self.packet)

    def test_all_core_types_describe_and_validate(self):
        schema = c.load_schema()
        values = {"shared_context": self.packet["context"], "plan_result": self.plan,
                  "critique_result": self.packet["critique"], "run_record": self.packet["run_record"][0],
                  "range": self.plan["completion_months"], "evidence": self.packet["context"]["evidence"][0],
                  "decision_packet": self.packet, "strategy_task": {"strategy_id": "boundary", "context_revision": 1,
                  "direction": "Introduce boundary", "design_difference": "Preserve internals", "weakness": "Debt remains"}}
        for name, value in values.items():
            with self.subTest(name=name):
                subset = c.describe(name, schema)
                c.audit_schema(subset, subset)
                c.validate(value, name)
                c.schema_validate(value, subset, subset)

    def test_describe_is_transitive_not_entire_schema(self):
        subset = c.describe("strategy_task", c.load_schema())
        self.assertEqual(set(subset["$defs"]), {"strategy_task", "text", "revision"})

    def test_unknown_type_rejected(self):
        with self.assertRaises(c.ContractError):
            c.validate({}, "not-a-type")

    def test_unsupported_schema_keyword_fails_closed(self):
        schema = c.load_schema()
        schema["$defs"]["range"]["oneOf"] = []
        with self.assertRaises(c.ContractError) as caught:
            c.validate(self.packet, schema=schema)
        self.assertEqual(caught.exception.code, "schema")

    def test_remote_schema_ref_rejected(self):
        schema = c.load_schema()
        schema["$defs"]["text"] = {"$ref": "https://example.invalid/schema"}
        with self.assertRaises(c.ContractError):
            c.validate(self.packet, schema=schema)

    def test_validation_ref_siblings_rejected(self):
        schema = c.load_schema()
        schema["$defs"]["text"] = {"$ref": "#/$defs/revision", "minimum": 8}
        with self.assertRaises(c.ContractError):
            c.validate(self.packet, schema=schema)

    def test_nonfinite_constants_and_overflow_rejected(self):
        for number in ("NaN", "Infinity", "-Infinity", "1e999"):
            with self.subTest(number=number), self.assertRaises(c.ContractError):
                c.loads('{"number":' + number + '}')

    def test_in_memory_nonfinite_rejected(self):
        self.packet["context"]["horizon_months"] = float("nan")
        self.rejects("nonfinite")

    def test_duplicate_json_keys_rejected_at_any_depth(self):
        with self.assertRaises(c.ContractError) as caught:
            c.loads('{"outer":{"value":1,"value":2}}')
        self.assertEqual(caught.exception.code, "duplicate_key")

    def test_reversed_range_rejected(self):
        self.plan["costs"][0]["hours"]["low"] = 100
        self.rejects("range")

    def test_partial_null_range_rejected(self):
        self.plan["costs"][0]["hours"]["reference"] = None
        self.rejects("range")

    def test_unknown_range_requires_reason(self):
        value = unknown(self.plan["costs"][0]["hours"])
        value["reason"] = "  "
        self.plan["costs"][0]["hours"] = value
        self.rejects("unknown_reason")

    def test_known_range_requires_evidence_or_assumption(self):
        value = self.plan["costs"][0]["hours"]
        value["evidence_ids"], value["assumption_ids"] = [], []
        self.rejects("basis")

    def test_boolean_is_not_number(self):
        self.plan["costs"][0]["hours"]["low"] = False
        self.rejects("type")

    def test_boolean_is_not_revision(self):
        self.plan["plan_revision"] = True
        self.rejects("type")

    def test_boolean_is_not_severity(self):
        self.plan["risks"][0]["residual_severity"] = True
        self.rejects("type")

    def test_negative_completion_rejected(self):
        self.plan["completion_months"]["low"] = -1
        self.rejects("minimum")

    def test_risk_severity_outside_ordinal_range_rejected(self):
        self.plan["risks"][0]["residual_severity"] = 6
        self.rejects("maximum")

    def test_unit_mismatch_rejected(self):
        for target, unit in (("monthly_savings_hours", "person_hour"), ("completion_months", "day")):
            with self.subTest(target=target):
                packet = fixture()
                packet["plans"][0][target]["unit"] = unit
                with self.assertRaises(c.ContractError) as caught:
                    c.validate(packet)
                self.assertEqual(caught.exception.code, "unit")

    def test_cost_unit_mismatch_rejected(self):
        self.plan["costs"][0]["hours"]["unit"] = "day"
        self.rejects("unit")

    def test_risk_recovery_unit_mismatch_rejected(self):
        self.plan["risks"][0]["recovery_hours"]["unit"] = "month"
        self.rejects("unit")

    def test_evidence_reference_rejected(self):
        self.plan["costs"][0]["hours"]["evidence_ids"] = ["missing"]
        self.rejects("reference")

    def test_assumption_reference_rejected(self):
        self.plan["monthly_savings_hours"]["assumption_ids"] = ["missing"]
        self.rejects("reference")

    def test_unknown_reference_rejected(self):
        self.plan["unknown_ids"] = ["missing"]
        self.rejects("reference")

    def test_constraint_reference_rejected(self):
        self.plan["gates"][0]["constraint_id"] = "missing"
        self.rejects("reference")

    def test_duplicate_plan_ids_rejected(self):
        self.packet["plans"][1]["id"] = "A"
        self.rejects("duplicate_id")

    def test_duplicate_strategy_ids_rejected(self):
        self.packet["plans"][1]["strategy_id"] = "boundary"
        self.rejects("duplicate_id")

    def test_duplicate_cost_component_ids_rejected(self):
        self.plan["costs"].append(copy.deepcopy(self.plan["costs"][0]))
        self.rejects("duplicate_id")

    def test_duplicate_evidence_registry_ids_rejected(self):
        self.packet["context"]["evidence"].append(copy.deepcopy(self.packet["context"]["evidence"][0]))
        self.rejects("duplicate_id")

    def test_duplicate_reference_ids_rejected(self):
        self.plan["evidence_ids"] = ["E1", "E1"]
        self.rejects("duplicate_id")

    def test_stale_plan_context_rejected(self):
        self.plan["context_revision"] = 2
        self.rejects("stale")

    def test_stale_critique_context_rejected(self):
        self.packet["critique"]["context_revision"] = 2
        self.rejects("stale")

    def test_stale_critique_plan_revision_rejected(self):
        self.plan["plan_revision"] = 2
        self.rejects("stale")

    def test_stale_decision_context_rejected(self):
        self.packet["decision"]["context_revision"] = 2
        self.rejects("stale")

    def test_stale_run_context_rejected(self):
        self.packet["run_record"][0]["context_revision"] = 2
        self.rejects("stale")

    def test_critic_must_review_baseline_too(self):
        self.packet["critique"]["reviewed_plans"].pop(0)
        self.rejects("reference")

    def test_finding_plan_reference_rejected(self):
        self.packet["critique"]["findings"][0]["plan_id"] = "missing"
        self.rejects("reference")

    def test_cycle_rejected(self):
        self.plan["steps"][0]["depends_on"] = ["S2"]
        self.rejects("cycle")

    def test_forward_dependency_accepted(self):
        self.plan["steps"].reverse()
        c.validate(self.packet)

    def test_self_dependency_rejected(self):
        self.plan["steps"][0]["depends_on"] = ["S1"]
        self.rejects("cycle")

    def test_missing_dependency_rejected(self):
        self.plan["steps"][0]["depends_on"] = ["missing"]
        self.rejects("reference")

    def test_excluded_cannot_be_recommended(self):
        self.plan["gates"][0]["status"] = "fail"
        self.packet["recommendation"]["plan_id"] = "A"
        self.rejects("excluded")

    def test_excluded_cannot_be_selected(self):
        self.plan["status"] = "infeasible"
        self.packet["decision"].update(status="selected", plan_id="A", answer="Choose A")
        self.rejects("excluded")

    def test_pending_cannot_have_answer_or_plan(self):
        self.packet["decision"]["answer"] = "Choose A"
        self.rejects("decision")

    def test_selection_requires_explicit_answer(self):
        self.packet["decision"].update(status="selected", plan_id="A")
        self.rejects("decision")

    def test_selected_valid_current_plan(self):
        self.packet["decision"].update(status="selected", plan_id="A", answer="I choose A; planning only.")
        c.validate(self.packet)

    def test_deferred_and_rejected_need_answer_not_plan(self):
        for status in ("deferred", "rejected"):
            with self.subTest(status=status):
                self.packet["decision"].update(status=status, plan_id=None, answer="Wait for measurements.")
                c.validate(self.packet)
                self.packet["decision"]["plan_id"] = "A"
                self.rejects("decision")

    def test_unknown_selection_reference_rejected(self):
        self.packet["decision"].update(status="selected", plan_id="missing", answer="Choose missing")
        self.rejects("reference")

    def test_unknown_recommendation_reference_rejected(self):
        self.packet["recommendation"]["plan_id"] = "missing"
        self.rejects("reference")

    def test_conditional_recommendation_needs_conditions(self):
        self.plan["gates"][0]["status"] = "unknown"
        self.packet["recommendation"].update(plan_id="A", conditions=[])
        self.rejects("recommendation")

    def test_planner_records_need_same_batch(self):
        self.packet["run_record"][1]["batch_id"] = "other-batch"
        self.rejects("trace")

    def test_planners_need_distinct_contexts(self):
        self.packet["run_record"][1]["context_id"] = self.packet["run_record"][0]["context_id"]
        self.rejects("trace")

    def test_critic_needs_independent_context(self):
        self.packet["run_record"][2]["context_id"] = self.packet["run_record"][0]["context_id"]
        self.rejects("trace")

    def test_failed_planner_does_not_satisfy_completion(self):
        self.packet["run_record"][0]["status"] = "failed"
        self.rejects("trace")

    def test_failed_critic_does_not_satisfy_completion(self):
        self.packet["run_record"][2]["status"] = "failed"
        self.rejects("trace")

    def test_nonviable_candidate_still_counts_as_strategy(self):
        self.plan["status"] = "infeasible"
        c.validate(self.packet)

    def test_run_strategy_must_align(self):
        self.packet["run_record"][0]["strategy_id"] = "missing"
        self.rejects("reference")

    def test_baseline_delta_cannot_be_nonzero(self):
        self.packet["baseline"]["costs"][0]["hours"]["high"] = 1
        self.rejects("baseline")

    def test_baseline_cannot_have_unknown_delta(self):
        self.packet["baseline"]["monthly_savings_hours"] = unknown(self.packet["baseline"]["monthly_savings_hours"])
        self.rejects("baseline")

    def test_unknown_extra_fields_rejected(self):
        self.plan["implementation_approved"] = True
        self.rejects("additional_property")

    def test_cli_help_does_not_read_stdin(self):
        result = self.cli("--help", text="not-json")
        self.assertEqual(result.returncode, 0)
        self.assertIn("describe", result.stdout)
        self.assertFalse(result.stderr)

    def test_cli_describe_does_not_read_stdin(self):
        result = self.cli("describe", "--type", "range", text="not-json")
        self.assertEqual(result.returncode, 0)
        self.assertIn("range", json.loads(result.stdout)["$defs"])

    def test_cli_bad_json_has_structured_error_without_traceback(self):
        result = self.cli("compare", text="{not-json}")
        self.assertEqual(result.returncode, 2)
        self.assertFalse(result.stdout)
        self.assertEqual(json.loads(result.stderr)["error"]["code"], "json")
        self.assertNotIn("Traceback", result.stderr)

    def test_cli_bad_arguments_have_structured_error(self):
        result = self.cli("validate", "--unknown")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stderr)["error"]["code"], "arguments")

    def test_cli_validation_reports_success(self):
        result = self.cli("validate", "--type", "decision_packet")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)["valid"])


if __name__ == "__main__":
    unittest.main()
