from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class LLMService:

    def analyze_with_context(self, user_question: str, context_chunks: list[str]):
        context_text = "\n".join(
            [f"- {chunk}" for chunk in context_chunks]
        )

        prompt = f"""
Eres un asistente experto en analítica bancaria.

Tu tarea es responder la pregunta del usuario usando el contexto recuperado desde la base de conocimiento.

Reglas:
1. Responde usando principalmente el contexto.
2. Si el contexto no es suficiente, dilo claramente.
3. No inventes información.
4. Devuelve SOLO JSON válido.

Pregunta del usuario:
{user_question}

Contexto recuperado:
{context_text}

Devuelve este formato JSON:
{{
  "answer": "respuesta final en lenguaje natural",
  "summary": "resumen breve",
  "main_topics": ["tema1", "tema2"],
  "used_context": ["fragmento1", "fragmento2"]
}}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        output = response.choices[0].message.content

        try:
            return json.loads(output)
        except Exception:
            return {
                "error": "El modelo no devolvió JSON válido",
                "raw_output": output
            }