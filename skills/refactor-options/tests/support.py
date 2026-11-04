"""Load only the bundled calculator, never application modules."""

import copy
import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("refactor_options_compare", ROOT / "scripts" / "compare.py")
calculator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(calculator)


def fixture():
    return calculator.loads((ROOT / "assets" / "example-decision.json").read_text(encoding="utf-8"))


def unknown(value):
    result = copy.deepcopy(value)
    for key in calculator.SCENARIOS:
        result[key] = None
    result["reason"] = "Not measured; collect evidence before estimating."
    return result


def row(packet, plan_id="A"):
    return next(item for item in packet["assessment"]["plans"] if item["plan_id"] == plan_id)
