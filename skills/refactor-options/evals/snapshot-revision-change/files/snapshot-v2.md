# Supplied current snapshot, context revision 2

checkout_total still uses standard=0.20/reduced=0.08. invoice_total now uses standard=0.19/reduced=0.07 under a distinct invoicing contract. Both public names, tuple order, rounding and error behavior must remain, including this newly required rule difference.

The entry points now ship as independently versioned packages. No shared-runtime library versioning or simultaneous rollback protocol is provided. A single identical rate function/body is no longer sufficient without explicit policy ownership and compatibility design. The refactor scope does not authorize changing rates to make them equal again.

No new effort estimates, frequency observations or executed regressions are available. The old approval does not express acceptance of these changed conditions.
