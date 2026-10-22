# Trace Matrix: Message Guard

Generated 2026-10-22 11:48 by `tools/trace.py` 1.0 from `specs/conops.md`, `specs/requirements.md`, `specs/scenarios.json`, `specs/glossary.md` and `reference/elicitation.md`; citations from 29 collected tests (16 cite a clause). Repository state: HEAD a0e0623, 23 changed or untracked path(s).

**Scope**: every declared link, in both directions. The tool decides whether a link resolves, not whether the linked texts agree; that review is rule SQ-2's.

## Forward: story to requirements to scenarios to tests

| Story | Source | Requirements | Scenarios | Tests citing the story | Tests citing its requirements |
|---|---|---|---|---|---|
| US-1 | E-3 | REQ-3 | SC-1, SC-2 | `test_scenarios.py::test_scenario[SC-1]`<br>`test_scenarios.py::test_scenario[SC-2]` | `test_filter.py::test_public_passes_unchanged` |
| US-2 | E-3 | REQ-2 | SC-3, SC-4 | `test_scenarios.py::test_scenario[SC-3]`<br>`test_scenarios.py::test_scenario[SC-4]` | `test_filter.py::test_restricted_passes_unchanged` |
| US-3 | E-1 | REQ-1 | SC-5, SC-6 | `test_scenarios.py::test_scenario[SC-5]`<br>`test_scenarios.py::test_scenario[SC-6]` | `test_filter.py::test_critical_is_dropped[-5]`<br>`test_filter.py::test_critical_is_dropped[0]`<br>`test_filter.py::test_critical_is_dropped[100]` |

## Backward: requirement to its derivation and its tests

| Requirement | Pattern | Derived from | Tests citing it |
|---|---|---|---|
| REQ-0 | ubiquitous | Glossary: message, security level, payload | `test_message.py::test_exactly_three_security_levels`<br>`test_message.py::test_level_must_be_a_security_level`<br>`test_message.py::test_message_does_not_change_after_creation`<br>`test_message.py::test_payload_must_be_an_integer`<br>`test_message.py::test_unknown_level_is_rejected` |
| REQ-1 | event-driven | US-3 | `test_filter.py::test_critical_is_dropped[-5]`<br>`test_filter.py::test_critical_is_dropped[0]`<br>`test_filter.py::test_critical_is_dropped[100]` |
| REQ-2 | event-driven | US-2 | `test_filter.py::test_restricted_passes_unchanged` |
| REQ-3 | event-driven | US-1 | `test_filter.py::test_public_passes_unchanged` |

## Backward: test to the clauses it cites

| Test | Clauses |
|---|---|
| `test_filter.py::test_critical_is_dropped[-5]` | REQ-1 |
| `test_filter.py::test_critical_is_dropped[0]` | REQ-1 |
| `test_filter.py::test_critical_is_dropped[100]` | REQ-1 |
| `test_filter.py::test_public_passes_unchanged` | REQ-3 |
| `test_filter.py::test_restricted_passes_unchanged` | REQ-2 |
| `test_message.py::test_exactly_three_security_levels` | REQ-0 |
| `test_message.py::test_level_must_be_a_security_level` | REQ-0 |
| `test_message.py::test_message_does_not_change_after_creation` | REQ-0 |
| `test_message.py::test_payload_must_be_an_integer` | REQ-0 |
| `test_message.py::test_unknown_level_is_rejected` | REQ-0 |
| `test_scenarios.py::test_scenario[SC-1]` | US-1 |
| `test_scenarios.py::test_scenario[SC-2]` | US-1 |
| `test_scenarios.py::test_scenario[SC-3]` | US-2 |
| `test_scenarios.py::test_scenario[SC-4]` | US-2 |
| `test_scenarios.py::test_scenario[SC-5]` | US-3 |
| `test_scenarios.py::test_scenario[SC-6]` | US-3 |

## Findings

None.
