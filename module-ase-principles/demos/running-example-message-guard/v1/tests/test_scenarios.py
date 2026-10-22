"""Evidence for the user stories: every acceptance scenario of specs/scenarios.json, run as a test.

The scenario file is a specification (values only, readable by a stakeholder, portable to any
realization); this loader binds each scenario to this realization's interface and cites the story
the scenario derives from, so the conformance report shows the story's evidence. The file is never
edited to make a test pass: a scenario that looks wrong is a gap about the pair (scenario, story).
"""

import json
from pathlib import Path

import pytest

from guard import Message, SecurityLevel, filter_message

SCENARIOS = Path(__file__).resolve().parent.parent / "specs" / "scenarios.json"


def _cases():
    data = json.loads(SCENARIOS.read_text(encoding="utf-8"))
    for scenario in data["scenarios"]:
        yield pytest.param(scenario, id=scenario["id"], marks=pytest.mark.req(scenario["derived_from"]))


@pytest.mark.parametrize("scenario", list(_cases()))
def test_scenario(scenario):
    given = scenario["input"]
    out = filter_message(Message(SecurityLevel(given["level"]), given["payload"]))
    expected = scenario["expected"]
    if expected is None:
        assert out is None
    else:
        assert out is not None
        assert (out.level.value, out.payload) == (expected["level"], expected["payload"])
