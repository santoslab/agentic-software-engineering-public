"""The spec-ID reader finds exactly the IDs spec.md defines.

If the spec gains or loses an ID, this test is updated together with the spec's CHANGELOG.
"""

from tests.conformance import spec_ids


def test_spec_ids_match_the_spec():
    ids = spec_ids()
    assert ids["Functional Requirements"] == [f"FR-{n:03d}" for n in range(1, 21)]
    assert ids["Success Criteria"] == [f"SC-{n:03d}" for n in range(1, 7)]
    assert ids["Acceptance Scenarios"] == (
        [f"US1-{n}" for n in range(1, 8)]
        + [f"US2-{n}" for n in range(1, 8)]
        + [f"US3-{n}" for n in range(1, 7)]
    )
    assert ids["Edge Cases"] == [
        "EDGE-occupied-square",
        "EDGE-out-of-range-square",
        "EDGE-unreadable-input",
        "EDGE-invalid-menu-choice",
        "EDGE-more-than-five-in-a-row",
        "EDGE-win-on-the-last-square",
        "EDGE-two-lines-at-once",
        "EDGE-end-of-input-or-interrupt",
    ]
