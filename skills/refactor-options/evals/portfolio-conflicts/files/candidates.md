# Fictional proposed boundaries, context revision 2

The current two public eligibility functions duplicate category checks and result construction. Signatures, comparison order, results and ValueError behavior must remain unchanged. A separate publish function calls eligibility, then one synchronous send; exceptions propagate.

- A: extract category validation into a shared runtime policy function. Each public eligibility function keeps its own result construction. New policy is initially unused; switch callers one by one, characterize old/new behavior and preserve adopted categories during recovery.
- B: extract validation and result construction into a shared runtime core. Both public functions become compatible wrappers. Add unused core, switch one then both, verify contracts/import, and recover coherent package versions preserving adopted categories.
- C: extract notification formatting and send dependency into a notification boundary while retaining the public publish signature, its existing eligibility call and send order/count. Add unused boundary, characterize send/failure traces, switch, and recover only notification changes.

A and B are complete alternative ownership choices for the same functions; this review is not asking to synthesize a new hybrid. C uses only the unchanged public eligibility contract, not A/B internals. C's orchestration verification may overlap with either route. All costs and executed verification are unknown.
