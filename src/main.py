# src/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.procesar_documentos import router as documentos_router

app = FastAPI()

# Configuración de CORS
# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite solicitudes desde cualquier dominio
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

# Incluir las rutas en la aplicación
app.include_router(documentos_router, prefix="/api", tags=["Documentos"])

# Ejecutar con: uvicorn app.main:app --reload
