# cynic/web/main.py

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlmodel import SQLModel, create_engine, Session, select
from alembic.config import Config
from alembic import command

from cynic.analyzer import CynicAnalyzer
from cynic.db.models import HallOfFameEntry

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, "cynic_database.db")}"

engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


class AnalyseRequest(BaseModel):
    """Modèle pour les données de la requête d'analyse."""

    contexte: str
    reponse: str
    proposer_au_palmares: bool = False


class AnalyseResponse(BaseModel):
    """Modèle pour les données de la réponse d'analyse."""

    score: int
    verdict: str
    expressions_cyniques: list[str]


# --- Initialisation de l'application FastAPI ---
app = FastAPI(
    title="Cynic API",
    description="API pour le Détecteur de Moquerie.",
    version="1.1.0",
)


@app.on_event("startup")
def on_startup():
    init_db()


# --- Chargement de la clé API Mistral depuis les variables d'environnement ---
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
analyzer = CynicAnalyzer(api_key=MISTRAL_API_KEY) if MISTRAL_API_KEY else None

if not analyzer:
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

    # Si l'utilisateur a coché la case et que le score est "intéressant"
    if request_data.proposer_au_palmares and result.get("score", 0) >= 7:
        with Session(engine) as session:
            db_entry = HallOfFameEntry.model_validate(
                result,
                update={
                    "contexte": request_data.contexte,
                    "reponse": request_data.reponse,
                },
            )
            session.add(db_entry)
            session.commit()

    return result


@app.get("/api/hall-of-fame", response_model=list[HallOfFameEntry])
async def get_hall_of_fame():
    with Session(engine) as session:
        statement = (
            select(HallOfFameEntry).order_by(HallOfFameEntry.score.desc()).limit(10)
        )
        results = session.exec(statement).all()
        return results


# --- Service de l'interface Web (Frontend) ---

# Monter le dossier 'static' pour qu'il soit accessible via le web
app.mount("/static", StaticFiles(directory="cynic/web/static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Sert la page principale de l'interface utilisateur.
    """
    return FileResponse("cynic/web/static/index.html")


@app.get("/hall-of-fame", response_class=HTMLResponse)
async def read_hall_of_fame_page(request: Request):
    return FileResponse("cynic/web/static/hall-of-fame.html")
