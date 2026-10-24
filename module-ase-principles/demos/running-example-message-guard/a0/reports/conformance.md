# Conformance Report: Message Guard

Generated 2026-10-24 11:48 by the plugin in `tests/conftest.py` from the clauses in `specs/conops.md`, `specs/requirements.md`; 10 tests cite a clause.

**Requirements coverage**: 4 of 4 test clauses have passing evidence.

| Clause | Specification | Method | Tests citing it | Status |
|---|---|---|---|---|
| US-1 | `conops.md` | walkthrough | — | walkthrough: see `records/walkthrough.md` |
| US-2 | `conops.md` | walkthrough | — | walkthrough: see `records/walkthrough.md` |
| US-3 | `conops.md` | walkthrough | — | walkthrough: see `records/walkthrough.md` |
| REQ-0 | `requirements.md` | test | `test_message.py::test_exactly_three_security_levels`<br>`test_message.py::test_unknown_level_is_rejected`<br>`test_message.py::test_level_must_be_a_security_level`<br>`test_message.py::test_payload_must_be_an_integer`<br>`test_message.py::test_message_does_not_change_after_creation` | pass |
| REQ-1 | `requirements.md` | test | `test_filter.py::test_critical_is_dropped[0]`<br>`test_filter.py::test_critical_is_dropped[100]`<br>`test_filter.py::test_critical_is_dropped[-5]` | pass |
| REQ-2 | `requirements.md` | test | `test_filter.py::test_restricted_passes_unchanged` | pass |
| REQ-3 | `requirements.md` | test | `test_filter.py::test_public_passes_unchanged` | pass |

Status of a *test* clause: **pass**, every citing test passed; **FAIL**, a citing test failed; **partial**, a citing test was skipped or not run; **no evidence**, no test cites the clause. A *walkthrough* clause is not decided by this run; its record is the walkthrough file.

## Unknown identifiers

None.
