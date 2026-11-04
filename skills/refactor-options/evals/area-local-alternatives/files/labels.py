def screen_label(kind):
    if kind == "new":
        return "New"
    if kind == "used":
        return "Used"
    raise ValueError("unsupported kind")


def export_label(kind):
    if kind == "new":
        return "New"
    if kind == "used":
        return "Used"
    raise ValueError("unsupported kind")


def publish(kind, sender):
    text = export_label(kind)
    sender.send(text)
    return text
