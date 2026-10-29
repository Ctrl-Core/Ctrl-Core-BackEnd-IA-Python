from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Dict
from .service import ActionPlanService

router = APIRouter(prefix="/api/ai/planes", tags=["Planes de Acción IA"])

class GeneratePlanRequest(BaseModel):
    razon_social: str
    sector: str
    brechas: Dict[str, float] # Ej: {"Estrategia": 4.5, "Digital": 2.1, "Financiera": 1.8}

@router.post("/generate")
def generate_plan(request: GeneratePlanRequest, x_tenant_id: int = Header(...)):
    try:
        plan = ActionPlanService.generate_plan(
            razon_social=request.razon_social,
            sector=request.sector,
            brechas=request.brechas
        )
        return {
            "success": True,
            "tenant_id": x_tenant_id,
            "plan_ia": plan
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))