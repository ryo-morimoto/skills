# Fictional same-target candidates

Two public functions duplicate category validation and arithmetic. Preserve public signatures, ordered equality comparisons, the (total,tax) result, existing float rounding and ValueError message. Both modules deploy as one package. The goal is one authored rate policy.

- A: "minimal policy". Move the original category branch unchanged to an internal rate function. Keep arithmetic in both public functions. Add unused helper, switch both paths in sequence, then retire old branches. Verify independent contract expectations, imports and adopted-category recovery. Uncalibrated cost assumption: 4–8 hours.
- B: "domain service". Exactly A's responsibility, inputs/outputs, dependency direction, switch steps, tests and recovery. Only the helper file/function name and proposal label differ. No added abstraction or work. Uncalibrated cost assumption: 8–12 hours.
- C: "calculation core". Move validation and the entire unchanged arithmetic sequence into a shared core; keep public compatibility wrappers. Add unused core, switch wrappers in sequence, then retire old implementations. Verify independent contracts/imports and adopted-category recovery. Cost unknown.

No tests ran. No domain rule or required contract differs across proposals. P0 leaves the two existing branches untouched, with zero incremental investment/saving but unmeasured absolute maintenance.
