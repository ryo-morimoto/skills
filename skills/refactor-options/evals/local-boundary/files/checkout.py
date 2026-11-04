def checkout_total(subtotal: float, category: str) -> tuple[float, float]:
    if category == "standard":
        rate = 0.20
    elif category == "reduced":
        rate = 0.08
    else:
        raise ValueError("unsupported tax category")
    tax = round(subtotal * rate, 2)
    return round(subtotal + tax, 2), tax
