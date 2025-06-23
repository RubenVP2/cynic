# cynic/web/main.py

import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from cynic.analyzer import CynicAnalyzer


class AnalyseRequest(BaseModel):
    """Modèle pour les données de la requête d'analyse."""

    contexte: str
    reponse: str


class AnalyseResponse(BaseModel):
    """Modèle pour les données de la réponse d'analyse."""

    score: int
    verdict: str
    expressions_cyniques: list[str]


# --- Initialisation de l'application FastAPI ---
app = FastAPI(
    title="Cynic API", description="API pour le Détecteur de Moquerie.", version="1.0.0"
)

# --- Chargement de la clé API Mistral depuis les variables d'environnement ---
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# Création d'une instance unique de notre analyseur.
analyzer = None
if MISTRAL_API_KEY:
    try:
        analyzer = CynicAnalyzer(api_key=MISTRAL_API_KEY)
    except ValueError as e:
        print(f"Erreur d'initialisation de CynicAnalyzer : {e}")
        analyzer = None
else:
    print("Attention: La variable d'environnement MISTRAL_API_KEY n'est pas définie.")


# --- Endpoints de l'API ---


@app.post("/api/analyze", response_model=AnalyseResponse)
async def analyze_text(request_data: AnalyseRequest):
    """
    Endpoint principal pour analyser un texte.
    Il reçoit un JSON avec contexte/réponse et retourne le résultat.
    """
    if not analyzer:
        raise HTTPException(
            status_code=503,  # Service Unavailable
            detail="Le service d'analyse n'est pas disponible car la clé API Mistral n'est pas configurée sur le serveur.",
        )

    result = analyzer.analyze(request_data.contexte, request_data.reponse)
    return result


# --- Service de l'interface Web (Frontend) ---

# Monter le dossier 'static' pour qu'il soit accessible via le web
app.mount("/static", StaticFiles(directory="cynic/web/static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Sert la page principale de l'interface utilisateur.
    """
    return FileResponse("cynic/web/static/index.html")
