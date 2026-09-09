# Checkout demo project

A small checkout pricing library: `cart.py` sums item prices, `discount.py`
applies a threshold discount, and `test_checkout.py` holds the pytest tests.
Testing conventions live in `testing-guidelines.md`.

## Working rules

- Begin every reply with a line of the form `STATUS: <one short phrase>`.
- Read a file before you edit it.
- Never modify test files. If a test looks wrong, say so and stop.
- Tool reporting: immediately after each tool call, add a fenced `json` code
  block of the form
  `{"tool": "...", "arguments": {...}, "result": "<one-line summary>"}`
  so the people watching can follow every action.
- Run tests with `pytest -q`, and only when asked to run them.
- Keep `NOTES.md` current: whenever you complete or pause a task, update its
  Goal, Changes, Evidence, and Next steps sections.
