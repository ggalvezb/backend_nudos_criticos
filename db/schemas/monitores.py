def monitor_schema(user) -> dict:
    return {
        "id": str(user["_id"]),
        "Nombre": str(user["Nombre"]),
        "Usuario": str(user["Usuario"]),
        "Email": str(user["Email"]),
        "Password": str(user["Password"]),
        "Token": str(user["Token"]),
        "Decretos":list(user["Decretos"]),
        "Tipousuario":str(user["Tipousuario"])
    }

def monitores_schema(users) -> list:
    return [monitor_schema(user) for user in users]

