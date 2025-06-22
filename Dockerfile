# --- STAGE 1: Le "Builder" ---
FROM python:3.12-slim AS builder

WORKDIR /app

RUN pip install pip-tools

# On copie uniquement les fichiers nécessaires à l'installation des dépendances.
# Cela permet de profiter du cache de Docker : si ces fichiers ne changent pas,
# Docker n'exécutera pas à nouveau l'installation des dépendances.
COPY pyproject.toml .

# On compile les dépendances (coeur + web) dans un fichier requirements.txt optimisé.
# C'est plus robuste que 'pip install' directement.
RUN piptools compile --extra web -o requirements.txt pyproject.toml

# On crée un environnement virtuel et on y installe les dépendances.
# Cela nous permettra de copier uniquement cet environnement dans l'image finale.
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt


# --- STAGE 2: L'Image Finale ---
FROM python:3.12-slim AS final

# On crée un utilisateur non-root pour des raisons de sécurité.
RUN useradd --create-home --shell /bin/bash appuser
WORKDIR /home/appuser/app
USER appuser

COPY --from=builder /opt/venv /opt/venv

COPY --chown=appuser:appuser cynic/ ./cynic/

ENV PATH="/opt/venv/bin:$PATH"

# On expose le port 8000 sur lequel Uvicorn va écouter.
EXPOSE 8000

# La commande pour lancer l'application lorsque le conteneur démarre.
# On utilise --host 0.0.0.0 pour rendre l'application accessible de l'extérieur du conteneur.
CMD ["uvicorn", "cynic.web.main:app", "--host", "0.0.0.0", "--port", "8000"]