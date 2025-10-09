def proyecto_schema(user) -> dict:
    return {
        "id": str(user["_id"]),
        "Codigo": str(user["Codigo"]),
        "Decreto": str(user["Decreto"]),
        "Nombre_Proyecto": str(user["Nombre_Proyecto"]),
        "Monitor": str(user["Monitor"]),
        "Nudo_Critico": list(user["Nudo_Critico"]),
    }

def proyectos_schema(users) -> list:
    return [proyecto_schema(user) for user in users]