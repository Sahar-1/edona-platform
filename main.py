import os
from typing import List
from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
from sqlalchemy.orm import Session

# Imports des services BDD et S3
from database import engine, get_db, Base
from models import Item
from schemas import ItemCreate, ItemResponse
from s3_service import upload_item_image, create_s3_bucket

load_dotenv()

# Création des tables PostgreSQL au démarrage si elles n'existent pas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EDONA API - Mercado Ibérico",
    description="API de backend con moderación de objetos por Agente IA (ES/PT)",
    version="1.0.0"
)

# Initialisation du bucket S3 au démarrage de FastAPI
@app.on_event("startup")
def startup_event():
    create_s3_bucket()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ItemRequest(BaseModel):
    title: str
    description: str

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Servidor EDONA funcionando correctamente."}

# Modération d'un objet via l'agent IA OpenAI
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

# Récupérer la liste des objets depuis la BDD PostgreSQL
@app.get("/api/v1/items", response_model=List[ItemResponse])
def list_items(db: Session = Depends(get_db)):
    """
    Retourne la liste des dons/objets enregistrés dans PostgreSQL.
    """
    return db.query(Item).all()

# Créer un nouvel objet en BDD PostgreSQL avec son URL d'image S3
@app.post("/api/v1/items", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """
    Enregistre un objet dans la base de données PostgreSQL.
    """
    db_item = Item(
        title=item.title,
        description=item.description,
        image_url=item.image_url,
        status="pending"
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Upload d'image vers LocalStack S3
@app.post("/api/v1/items/upload")
async def upload_item_image_endpoint(file: UploadFile = File(...)):
    """
    Téléverse une image d'objet sur S3 et retourne son URL d'accès.
    """
    try:
        url = upload_item_image(file)
        return {"url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du téléversement de l'image: {str(e)}")