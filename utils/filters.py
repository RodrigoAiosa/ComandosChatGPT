def filter_commands(commands, search="", categories=None):
    """
    categories: None ou lista vazia = todas as categorias.
    Caso contrário, filtra pelas categorias informadas.
    """
    search = (search or "").strip().lower()
    result = commands
    if categories:
        result = [c for c in result if c["category"] in categories]
    if search:
        result = [
            c for c in result
            if search in c["command"].lower()
            or search in c["description"].lower()
            or search in c["example"].lower()
            or search in c["category"].lower()
        ]
    return result
