# app/routes/procesar_documentos.py
from fastapi import APIRouter, File, UploadFile
from typing import List
from src.services.document_service import procesar_y_comparar_documentos

router = APIRouter()

@router.post("/procesar-documentos/")
async def subir_documentos(files: List[UploadFile] = File(...)):
    """
    Endpoint para recibir los 5 archivos PDF, compararlos y generar un CSV.
    """
    return procesar_y_comparar_documentos(files)
