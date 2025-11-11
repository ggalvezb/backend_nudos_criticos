from pydantic import BaseModel
from typing import Optional

#Entidad users
class Monitor(BaseModel):
        id: Optional[str]
        Nombre: str
        Usuario: str
        Email: str
        Password: str
        Token: str
        Decretos:Optional[list]
        Tipousuario:str
        