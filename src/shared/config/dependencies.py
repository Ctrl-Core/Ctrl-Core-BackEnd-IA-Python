import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from google import genai

load_dotenv()

# Cliente Qdrant HTTP local
qdrant = QdrantClient(
    url=f"http://{os.getenv('QDRANT_HOST', 'localhost')}:{os.getenv('QDRANT_PORT', 6333)}",
    api_key=os.getenv("QDRANT_API_KEY")
)

# Forzar api_version='v1' para resolver embeddings sin conflicto de v1beta
ai_client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options={'api_version': 'v1'}
)

COLLECTION_NAME = "cde_companies"

try:
    qdrant.get_collection(COLLECTION_NAME)
except Exception:
    qdrant.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=768, distance=Distance.COSINE)
    )