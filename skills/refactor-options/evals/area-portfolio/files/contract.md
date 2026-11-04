# Synthetic multi-area planning fixture

- No customer data, execution logs, measured effort or change-frequency history is supplied.
- Keep public names, argument order/names, return values, error propagation and current float/round behavior.
- checkout_total/invoice_total return (total,tax); unsupported categories raise ValueError("unsupported tax category").
- place_order calls calculation, exactly one db.execute with the exact SQL and tuple, then exactly one mailer.send, then returns (total,tax).
- A calculation failure causes no database or mail call. A database exception prevents mail. A mail exception propagates after the database call, without retrying or compensating.
- No new transaction, retry, outbox, async send, commit, rollback, caching or idempotency behavior is authorized as behavior-preserving refactoring.
- preview_receipt has no external side effects and uses exactly the same message format as place_order.
- Both source files are distributed in one fictional package. Internal files may be proposed but not created during planning.
- Price-rule, persistence-boundary and notification changes are separate representative change scenarios; both persistence and notification currently touch place_order in orders.py.
- Different areas do not prove disjoint effort/benefit. All measurements and combined estimates remain unknown.
