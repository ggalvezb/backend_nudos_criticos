from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from db.client import db_client
from db.models.monitores import Monitor
from db.schemas.monitores import monitor_schema, monitores_schema
from bson import ObjectId
import routers.funciones as fun
#from routers.auth_user import oauth2

router=APIRouter(prefix="/monitor",tags=["Monitor"])
registro_bd=db_client.monitor

#Retorno todos los proyectos
@router.get("/", response_model=list[Monitor])
async def proyecto():
    return fun.retorno_todos_perfiles(monitores_schema,registro_bd)

#Agrego un proyecto a la BD
@router.post("/")
async def proyecto(beneficiario:Monitor):
    return fun.agrego_registro(Monitor,monitor_schema,beneficiario,"id",beneficiario.id,registro_bd)

#Elimino un proyecto de la BD
@router.delete("/{id}")
async def proyecto(id: str):
    return fun.elimino_registro(registro_bd,ObjectId(id))

#Reemplazo un proyecto de la BD
@router.put("/", response_model=Monitor,description="Esta funcion edita el proyecto por ID")
async def proyecto(proyecto:Monitor):
    registro_dict=dict(proyecto)
    del registro_dict["id"]
    try:
        registro_bd.find_one_and_replace({"_id": ObjectId(proyecto.id)}, registro_dict)
    except:
        return {"Error: No se a encontrado usuario"}
    return proyecto


#Edito un campo de un proyecto en la BD
@router.patch("/{id}/{campo_de_busqueda}",description="Esta funcion edita un campo del proyecto")
async def proyecto(id:str,campo_de_busqueda:str,proyecto:Monitor):
#def edito_registro_por_campo(dato,campo_de_busqueda,campo_a_buscar,base_datos):
    registro_dict=dict(proyecto)
    try:
        print("id:", id)
        print("campo_de_busqueda:", campo_de_busqueda)
        print("valor a actualizar:", registro_dict[campo_de_busqueda])
        registro_bd.update_one(
            {"_id": ObjectId(id)},   # Buscar por _id
            {"$set": {campo_de_busqueda: registro_dict[campo_de_busqueda]}}      # Solo actualiza ese campo
        )        

        return {"Proyecto Actualizado"}
    except(Exception) as e:
        print("Error: ", e)
        return {"Error: No se a encontrado usuario"}