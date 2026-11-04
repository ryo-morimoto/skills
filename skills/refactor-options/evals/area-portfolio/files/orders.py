from pricing import checkout_total, invoice_total


def place_order(order_id, subtotal, category, customer_email, db, mailer):
    total, tax = checkout_total(subtotal, category)
    db.execute("INSERT INTO orders VALUES (?, ?, ?)", (order_id, total, tax))
    message = f"Order {order_id}: total={total:.2f}; tax={tax:.2f}"
    mailer.send(customer_email, message)
    return total, tax


def preview_receipt(order_id, subtotal, category):
    total, tax = invoice_total(subtotal, category)
    return f"Order {order_id}: total={total:.2f}; tax={tax:.2f}"
