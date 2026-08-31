import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = FastAPI(
    title="EDONA API - Mercado Ibérico",
    description="API de backend con moderación de objetos por Agente IA (ES/PT)",
    version="1.0.0"
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ItemRequest(BaseModel):
    title: str
    description: str

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Servidor EDONA funcionando correctamente."}

@app.post("/api/v1/items/moderate")
def moderate_item(item: ItemRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": (
                        "Eres un agente moderador para EDONA, una plataforma de donación gratuita de objetos en España y Portugal. "
                        "Analiza el título y la descripción del objeto enviado. "
                        "Responde OBLIGATORIAMENTE en formato JSON estricto con dos claves: "
                        "'approved' (boolean: true o false) y 'reason' (string: explicación breve en ESPAÑOL). "
                        "Rechaza sistemáticamente armas, drogas, productos caducados, animales o contenido ilícito."
                    )
                },
                {
                    "role": "user", 
                    "content": f"Titre: {item.title}\nDescription: {item.description}"
                }
            ],
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la moderación: {str(e)}")