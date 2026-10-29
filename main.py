from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import src.shared.config.dependencies 

# Importa tus dos routers
from src.modules.deduplicacion.router import router as deduplicacion_router
from src.modules.investigador.router import router as planes_router # <--- NUEVO

app = FastAPI(title="CTRL+CORE AI Engine", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra los routers
app.include_router(deduplicacion_router)
app.include_router(planes_router) # <--- NUEVO

@app.get("/api/ai/health")
def health_check():
    return {"status": "AI Engine Online", "qdrant": "Connected"}