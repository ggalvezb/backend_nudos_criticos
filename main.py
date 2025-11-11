from fastapi import FastAPI
#from fastapi.staticfiles import StaticFiles
from routers import proyectos,monitores,auth_user
from fastapi.middleware.cors import CORSMiddleware
# Inicia el servidor: uvicorn main:app --reload

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las solicitudes (puedes restringirlo a dominios específicos)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#routers
app.include_router(proyectos.router)
app.include_router(monitores.router)
app.include_router(auth_user.router)

@app.get("/")
async def root():
    return{"message":"Hello World"}