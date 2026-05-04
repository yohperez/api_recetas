from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import recipes
from .database import engine, Base

# Crear las tablas al arrancar (muy común en repositorios de clase)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SaborScript API 🍳",
    description="API para la gestión de recetas de cocina - Proyecto Individual",
    version="1.0.0"
)

# Configuración de CORS (Permitir que el frontend se conecte)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, pon aquí la URL de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluimos el router con TAGS para que en Swagger salgan agrupados
app.include_router(recipes.router, prefix="/api/v1", tags=["Recetas"])

@app.get("/", tags=["Root"])
def read_root():
    return {"status": "online", "message": "Bienvenido a SaborScript API"}
