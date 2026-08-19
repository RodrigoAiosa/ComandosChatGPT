def filter_commands(commands, search="", category="Todas"):
    search = (search or "").strip().lower()
    result = commands
    if category != "Todas":
        result = [c for c in result if c["category"] == category]
    if search:
        result = [
            c for c in result
            if search in c["command"].lower()
            or search in c["description"].lower()
            or search in c["example"].lower()
            or search in c["category"].lower()
        ]
    return result
