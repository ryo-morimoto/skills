# Supplied historical snapshot, context revision 1

checkout_total and invoice_total use identical standard=0.20/reduced=0.08 rules, the same (total,tax) sequence, float rounding and ValueError message. Both modules ship in one package. A shared policy was considered behavior-preserving under these facts. No tests or calibrated cost/frequency measurements were supplied.
