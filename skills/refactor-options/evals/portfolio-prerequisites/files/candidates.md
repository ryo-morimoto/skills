# Fictional reviewed-plan input, not a completed decision packet

Context revision 4. P0 is no change. Existing public parse/send/save APIs remain unchanged.

- P1, input boundary: introduce an internal immutable Record with id/text fields and a legacy-to-Record adapter. Public parse still returns its legacy tuple. Add adapter unused, characterize it, then expose the internal port only after contract review. Recovery keeps old public behavior. This is the only supplied plan that introduces Record and its adapter.
- P2, persistence boundary: the proposed repository consumes Record.id/Record.text through P1's new internal port. It does not contain its own legacy adapter. It can be added unused, then connected after the port exists. SQL, values, counts and exceptions must match the legacy path. Removing P1 while P2 is active breaks that port.
- P3, notification boundary: extract a pure formatter that also consumes P1's Record port, with the existing synchronous sender called after save. It has no private adapter. No retry/outbox is added. Save and notification can each be switched separately once the port exists.

Each candidate has future characterization, unused-addition, switch, contract-check and boundary-specific recovery steps. Their static details still need critique; no tests have run. P2 and P3 touch the same orchestration file, but neither calls the other's new internal implementation. There is no stated P2-before-P3 requirement.
