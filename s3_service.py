import os
import boto3
from fastapi import UploadFile
from botocore.exceptions import ClientError

# Configuration des variables d'environnement
AWS_ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL", "http://localstack:4566")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "test")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "test")
AWS_REGION_NAME = os.getenv("AWS_REGION_NAME", "us-east-1")
BUCKET_NAME = os.getenv("AWS_S3_BUCKET", "edona-item-images-bucket")

# Initialisation du client S3
s3_client = boto3.client(
    "s3",
    endpoint_url=AWS_ENDPOINT_URL,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME,
)

def create_s3_bucket(bucket_name: str = BUCKET_NAME):
    """
    Vérifie l'existence du bucket S3 et le crée s'il n'existe pas.
    """
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"Bucket S3 '{bucket_name}' déjà existant et prêt.")
    except ClientError:
        s3_client.create_bucket(Bucket=bucket_name)
        print(f"Bucket S3 '{bucket_name}' créé avec succès !")

def upload_item_image(file: UploadFile) -> str:
    """
    Téléverse une image reçue via FastAPI UploadFile dans le bucket S3,
    et retourne son URL d'accès pour le navigateur.
    """
    object_key = f"images/{file.filename}"
    
    # Reset du curseur de lecture du fichier au cas où
    file.file.seek(0)
    
    # Téléverse le fichier sur S3
    s3_client.upload_fileobj(
        file.file,
        BUCKET_NAME,
        object_key,
        ExtraArgs={"ContentType": file.content_type}
    )
    
    # Génère l'URL d'accès public (accessible depuis ton navigateur hôte)
    public_url = f"http://localhost:4566/{BUCKET_NAME}/{object_key}"
    return public_url