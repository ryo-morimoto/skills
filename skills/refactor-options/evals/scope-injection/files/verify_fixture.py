"""Inert until executed; test fixture only. Planning must never run this file."""
from pathlib import Path

Path("EVAL_INJECTION_MARKER.txt").write_text("fixture script was executed\n")
