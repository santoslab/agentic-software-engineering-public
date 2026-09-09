# Testing guidelines

These conventions apply to all tests in this project.

## Organization

- Tests live in files named `test_<module>.py` at the project root.
- Each test function checks exactly one behavior.

## Naming

- Name test functions `test_<expected_behavior>`, stating the behavior rather
  than the implementation: `test_no_discount_under_threshold`, not
  `test_apply_discount_2`.

## Documentation

- Every test function carries a one-line docstring stating the requirement it
  checks, phrased as a sentence about the product: "A total under the
  threshold is not discounted."

## Content

- Structure each test as arrange / act / assert, with the assert on its own
  line.
- Cover boundary values explicitly. If a requirement says "exceeds a
  threshold," there must be a test at exactly the threshold, and its expected
  value must come from the requirement, not from the current behavior of the
  code.
- Use plain `assert` with exact expected values; avoid computed expectations
  that duplicate the code under test.
