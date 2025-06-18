# tests/test_analyzer.py

import pytest
from unittest.mock import patch, Mock
from cynic.analyzer import CynicAnalyzer


def test_analyze_successful_response():
    """
    Teste le cas où l'API Mistral retourne une réponse JSON valide.
    """
    # Mock : Simuler la réponse de l'API Mistral
    mock_choice = Mock()
    mock_choice.message.content = (
        '{"score": 8, "verdict": "Verdict de test, parfaitement cynique."}'
    )

    # On crée le mock pour l'objet de réponse global
    mock_api_response = Mock()
    mock_api_response.choices = [mock_choice]

    # Patch : Remplacer l'appel à l'API Mistral par notre réponse simulée
    with patch(
        "cynic.analyzer.Mistral.chat.complete", return_value=mock_api_response
    ) as mock_api_call:

        analyzer = CynicAnalyzer(api_key="fake_key_for_testing")
        resultat = analyzer.analyze(
            contexte="Un contexte sans importance",
            reponse="Une réponse sans importance",
        )

        # Assertions : Vérifier que le résultat est conforme aux attentes
        assert isinstance(resultat, dict)
        assert "score" in resultat
        assert "verdict" in resultat
        assert resultat["score"] == 8
        assert resultat["verdict"] == "Verdict de test, parfaitement cynique."

        # Bonus : Mais si tu as lu jusqu'ici, tu es un vrai fan !
        mock_api_call.assert_called_once()
