# cynic/analyzer.py

import json
from mistralai.client import Mistral
from .prompts import PROMPT_SYSTEME


class CynicAnalyzer:
    """
    Cette classe permet d'analyser des réponses pour détecter le cynisme ou la moquerie
    en utilisant un modèle Mistral. Elle gère la connexion à l'API et le formatage des requêtes.
    Elle fournit une méthode `analyze` qui prend un contexte et une réponse, et retourne
    un score et un verdict de cynisme.
    """

    def __init__(self, api_key: str, model: str = "mistral-large-latest"):
        """
        Constructeur de la classe CynicAnalyzer.
        Initialise le client Mistral avec la clé API fournie et le modèle spécifié.

        Args:
            api_key (str): La clé API Mistral pour s'authentifier.
            model (str): Le nom du modèle Mistral à utiliser.
        """
        if not api_key:
            raise ValueError(
                "La clé API de Mistral est requise pour initialiser l'analyseur."
            )

        self.client = Mistral(api_key=api_key)
        self.model = model

    def analyze(self, contexte: str, reponse: str) -> dict:
        """
        Analyse une conversation et retourne un score et un verdict de cynisme.

        Args:
            contexte (str): Le contexte de la conversation.
            reponse (str): La réponse à analyser.
        """
        # Préparation des messages pour l'API Mistral
        messages = [
            {"role": "system", "content": PROMPT_SYSTEME},
            {
                "role": "user",
                "content": f'Voici la situation :\n\nContexte : "{contexte}"\n\nRéponse : "{reponse}"',
            },
        ]

        try:
            # Appel à l'API Mistral pour obtenir une réponse
            chat_response = self.client.chat.complete(
                model=self.model,
                messages=messages,
                response_format={"type": "json_object"},
            )

            reponse_json = chat_response.choices[0].message.content
            resultat = json.loads(reponse_json)
            return resultat

        except Exception as e:
            # TODO : Affiner la gestion d'erreur ici plus tard
            print(f"Une erreur est survenue lors de l'appel à l'API Mistral : {e}")
            return {
                "score": -1,
                "verdict": "Le Détecteur est en panne... Impossible de savoir si on se moque de vous.",
            }
