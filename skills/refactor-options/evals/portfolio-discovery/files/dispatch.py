def quote(parcel):
    if parcel["zone"] == "local":
        return parcel["weight"] * 2
    if parcel["zone"] == "remote":
        return parcel["weight"] * 4
    raise ValueError("unknown zone")


def preview(parcel):
    amount = quote(parcel)
    return f"Shipment {parcel['id']}: {amount:.2f}"


def dispatch(parcel, store, courier, audit):
    amount = quote(parcel)
    store.execute("INSERT INTO shipments VALUES (?, ?)", (parcel["id"], amount))
    receipt = courier.book(parcel["id"], amount)
    audit.write(f"Shipment {parcel['id']}: {amount:.2f}")
    return receipt
