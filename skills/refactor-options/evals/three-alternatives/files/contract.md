# Synthetic evaluation fixture, not application code

- Public names and signatures: checkout_total(subtotal, category), invoice_total(subtotal, category).
- Return tuple: (rounded total, rounded tax), in that order.
- Existing categories: standard = 0.20, reduced = 0.08.
- Unknown category: ValueError("unsupported tax category").
- Preserve current Python round behavior, including float inputs and boundary cases.
- Consumers deploy these two modules together as one fictional package.
- The fixture contains no measured effort, change frequency, savings, runtime logs or executed tests.
- A behavior-preserving refactor may add internal files in its PLAN; this task does not authorize edits.
- All costs and projected benefits must remain unknown or explicitly uncalibrated assumptions.
