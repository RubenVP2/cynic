# tests/test_analyzer.py
import json

from unittest.mock import patch, Mock
from cynic.analyzer import CynicAnalyzer


@patch("cynic.analyzer.Mistral")
def test_analyze_successful_response(mock_mistral_class):
    """
    Teste le cas d'une réponse réussie de l'API en construisant
    un mock qui respecte la structure de l'objet de réponse réel.
    """
    # 1. Préparation du Mock
    mock_api_response_content = json.dumps(
        {"score": 8, "verdict": "Le cynisme est palpable."}
    )

    # On crée un mock pour l'objet "message" le plus imbriqué
    mock_message = Mock()
    mock_message.content = mock_api_response_content

    # On crée un mock pour l'objet "choice" qui contient le message
    mock_choice = Mock()
    mock_choice.message = mock_message

    # On crée le mock de réponse final.
    # Son attribut "choices" est une VRAIE LISTE Python contenant notre mock_choice.
    mock_response = Mock()
    mock_response.choices = [mock_choice]

    # On configure le mock de la classe Mistral pour retourner notre mock_response
    mock_instance = mock_mistral_class.return_value
    mock_instance.chat.complete.return_value = mock_response

    # 2. Exécution du code à tester
    analyzer = CynicAnalyzer(api_key="fake_key_for_testing")
    resultat = analyzer.analyze(contexte="Un contexte", reponse="Une réponse")

    # 3. Assertions
    assert resultat["score"] == 8
    assert "palpable" in resultat["verdict"]
    mock_instance.chat.complete.assert_called_once()
