def display_name(value):
    if not value:
        raise ValueError("missing name")
    return value.strip()


def preview(value):
    return f"Registered: {display_name(value)}"


def register(value, store, sender):
    name = display_name(value)
    store.save(name)
    sender.send(f"Registered: {name}")
    return name
