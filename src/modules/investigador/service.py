import json
from google.genai import types
from src.shared.config.dependencies import ai_client

class ActionPlanService:
    @staticmethod
    def generate_plan(razon_social: str, sector: str, brechas: dict) -> dict:
        prompt = f"""
        Eres un consultor experto del Centro de Desarrollo Empresarial (CDE UNAB).
        Empresa: {razon_social} (Sector: {sector})
        Resultados del autodiagnóstico (Puntajes sobre 5.0):
        {json.dumps(brechas, indent=2)}

        Genera un plan de acción estratégico con las 3 tareas más urgentes (Kanban) enfocadas 
        en las áreas con puntajes más bajos (las mayores brechas).
        
        Devuelve ÚNICAMENTE un JSON con esta estructura exacta, sin markdown ni explicaciones:
        {{
          "tareas": [
            {{
              "titulo": "string (Ej: Implementar pasarela de pagos)",
              "descripcion": "string (Descripción táctica para el emprendedor)",
              "eje": "string (El nombre del eje afectado, Ej: Digital, Financiera)",
              "prioridad": "ALTA" | "MEDIA",
              "xp_recompensa": int (valores entre 100 y 300)
            }}
          ]
        }}
        """

        response = ai_client.models.generate_content(
            model='gemini-3.1-flash-lite', # Súper rápido y económico
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            ),
        )
        
        # Parseamos el JSON garantizado por Gemini
        return json.loads(response.text)