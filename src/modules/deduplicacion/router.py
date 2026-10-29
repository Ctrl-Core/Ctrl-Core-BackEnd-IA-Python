from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from .service import DeduplicacionService

router = APIRouter(prefix="/api/ai/empresas", tags=["Deduplicación Vectorial"])

class CheckDuplicateRequest(BaseModel):
    razon_social: str
    sector: str
    municipio: str

@router.post("/check-duplicate")
def check_duplicate(request: CheckDuplicateRequest, x_tenant_id: int = Header(...)):
    try:
        # Concatenamos los datos clave para capturar la semántica completa de la empresa
        texto_analisis = f"{request.razon_social} - {request.sector} - {request.municipio}"
        
        similares = DeduplicacionService.buscar_similares(
            tenant_id=x_tenant_id,
            texto_empresa=texto_analisis,
            umbral=0.82 # Sensibilidad ajustada
        )
        
        return {
            "success": True,
            "tenant_id": x_tenant_id,
            "is_duplicate_risk": len(similares) > 0,
            "matches": similares
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))