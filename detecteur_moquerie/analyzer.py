import os
import json
from mistralai import Mistral
from .prompts import PROMPT_SYSTEME

api_key = os.getenv("MISTRAL_API_KEY")

# Simple vérification de la clé API
if not api_key:
    raise ValueError(
        "La clé API de Mistral n'a pas été trouvée. Veuillez la définir avec la variable d'environnement MISTRAL_API_KEY."
    )

client = Mistral(api_key=api_key)


def analyser_reponse_avec_mistral(contexte: str, reponse: str) -> dict:
    """
    Cette fonction envoie la conversation à l'API Mistral et retourne le résultat.
    """
    # On choisit le modèle. 'mistral-large-latest' est très performant.
    # Pour économiser des coûts, 'mistral-small-latest' ou 'open-mistral-7b' sont de bonnes alternatives.
    model_a_utiliser = "mistral-large-latest"

    # On crée la liste des messages pour l'API
    messages = [
        {"role": "system", "content": PROMPT_SYSTEME},
        {
            "role": "user",
            "content": f'Voici la situation :\n\nContexte : "{contexte}"\n\nRéponse : "{reponse}"',
        },
    ]

    try:
        # On appelle l'API
        chat_response = client.chat.complete(
            model=model_a_utiliser,
            messages=messages,
            response_format={"type": "json_object"},  # On force la réponse en JSON
        )

        # On récupère le contenu de la réponse et on le transforme de texte JSON en dictionnaire Python
        reponse_json = chat_response.choices[0].message.content
        resultat = json.loads(reponse_json)
        return resultat

    except Exception as e:
        # En cas d'erreur avec l'API ou le format JSON
        print(f"Une erreur est survenue lors de l'appel à l'API Mistral : {e}")
        return {
            "score": -1,
            "verdict": "Le Détecteur est en panne... Impossible de savoir si on se moque de vous. C'est peut-être un signe.",
        }
