# On part de l'image python officielle
FROM python:3

# On définit un working directory
# toutes les opérations suivantes seront exécutées depuis ce dossier
WORKDIR /app

# On copie le fichier de dépendances dans l'image Docker
COPY ./requirements.txt .

# Installation des dépendances du code
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code dans l'image Docker
COPY ./app.py .

# On définit la commande à lancer lorsqu'on démarre un conteneur basé sur cette image
CMD ["python", "app.py"]
