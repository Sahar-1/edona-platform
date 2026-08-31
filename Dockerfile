# 1. Image de base Python légère
FROM python:3.11-slim

# 2. Définir le répertoire de travail dans le conteneur
WORKDIR /app

# 3. Empêcher Python d'écrire des fichiers .pyc et forcer l'affichage immédiat des logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. Copier d'abord les dépendances pour bénéficier du cache Docker
COPY requirements.txt .

# 5. Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copier tout le reste du code source
COPY . .

# 7. Exposer le port 8000
EXPOSE 8000

# 8. Commande de lancement de l'application FastAPI en production
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
