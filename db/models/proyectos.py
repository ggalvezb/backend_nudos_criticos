from pydantic import BaseModel
from typing import Optional

#Entidad users
class Proyecto(BaseModel):
        id: Optional[str]
        Codigo: str
        Decreto: str
        Nombre_Proyecto: str
        Monitor: str
        Nudo_Critico: Optional[list]