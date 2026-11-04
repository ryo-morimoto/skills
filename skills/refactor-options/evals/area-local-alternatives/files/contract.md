# Fictional labels package

- Preserve every public signature and the exact equality comparisons, labels and ValueError message.
- Unsupported values are not necessarily hashable; introducing a dict-only lookup may change errors.
- publish resolves a label first, calls sender.send once, discards its return value, then returns the label.
- Label failure causes no send. Send failure propagates with no retry or conversion.
- Rule ownership and sender dependency are separate improvement areas. No independent deployment requirement is known.
- Internal source or tooling may be proposed but never created/executed by the planner. Generator operations have real costs and ownership requirements.
