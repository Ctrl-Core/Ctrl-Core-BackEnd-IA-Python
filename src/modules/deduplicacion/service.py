from google.genai import types
from qdrant_client.models import Filter, FieldCondition, MatchValue
from src.shared.config.dependencies import qdrant, ai_client, COLLECTION_NAME

class DeduplicacionService:
    @staticmethod
    def generar_embedding(texto: str) -> list[float]:
        response = ai_client.models.embed_content(
            model="gemini-embedding-001",
            contents=texto,
            config=types.EmbedContentConfig(
                task_type="SEMANTIC_SIMILARITY",
                output_dimensionality=768
            )
        )
        # Se accede al primer elemento [0] de la lista de embeddings
        return response.embeddings[0].values

    @staticmethod
    def buscar_similares(tenant_id: int, texto_empresa: str, umbral: float = 0.82):
        vector = DeduplicacionService.generar_embedding(texto_empresa)

        # Se usa query_points y query=vector, accediendo a .points al final
        respuesta = qdrant.query_points(
            collection_name=COLLECTION_NAME,
            query=vector,
            query_filter=Filter(
                must=[
                    FieldCondition(
                        key="tenant_id",
                        match=MatchValue(value=tenant_id)
                    )
                ]
            ),
            limit=3,
            score_threshold=umbral
        )

        return [
            {
                "empresa_id": hit.payload.get("empresa_id") if hit.payload else None,
                "razon_social": hit.payload.get("razon_social") if hit.payload else "Desconocida",
                "similitud": round(hit.score, 4)
            }
            for hit in respuesta.points
        ]