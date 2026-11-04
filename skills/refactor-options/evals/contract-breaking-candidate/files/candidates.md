# Fictional proposals, not implemented code

Assume two public entry points currently contain source.py's body. Both signatures, ordered category comparisons, (total,tax), rounding and ValueError("unsupported tax category") are required contracts.

- A extracts only the original category branch into a shared function, preserving arithmetic locally. No lookup/type conversion is added.
- B extracts the entire original function body into a shared internal core; public wrappers return its result unchanged. No arithmetic or error changes are proposed.
- C also uses a core but its exact proposed body is:

```python
rates = {"standard": 0.20, "reduced": 0.08}
rate = rates[category]
tax = round(subtotal * rate, 2)
return tax, round(subtotal + tax, 2)
```

C's public wrappers neither reorder results nor convert exceptions. All three describe unused-addition, sequential switching, contract regression and package recovery, but these future tests have not run. Lower quoted cost is not permission to change behavior. Effort, frequency and savings are unknown.
