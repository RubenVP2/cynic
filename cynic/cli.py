# cynic/cli.py

import os
from time import sleep
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
from rich.syntax import Syntax
from .analyzer import CynicAnalyzer
from .prompts import PROMPT_SYSTEME


def main():
    console = Console()

    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        console.print(
            "[bold red]Erreur : La clé API de Mistral n'a pas été trouvée.[/bold red]"
        )
        console.print(
            "Veuillez la définir avec la variable d'environnement MISTRAL_API_KEY."
        )
        return  # On arrête le programme proprement

    try:
        # Affichage du titre et de l'instruction
        titre = Panel(
            Text(
                "🕵️‍♂️ Cynic (Powered by Mistral) 🕵️‍♀️",
                justify="center",
                style="bold magenta",
            ),
            title="[bold cyan]Bienvenue[/bold cyan]",
            subtitle="[bold cyan]L'IA qui vous dit la vérité, même quand ça fait mal.[/bold cyan]",
        )
        console.print(titre)
        console.print(
            Panel(
                Syntax(PROMPT_SYSTEME, "markdown", theme="dracula", word_wrap=True),
                title="[bold yellow]Instruction donnée à l'IA[/bold yellow]",
            )
        )
        # Première interaction avec l'utilisateur : demander le contexte
        console.print("\nPour commencer, décris la situation.", style="bold blue")

        contexte_user = Prompt.ask(
            "[cyan]Quel était le message ou la question d'origine ?[/cyan]"
        )

        # Deuxième interaction avec l'utilisateur : demander la réponse reçue
        console.print(
            "\nMaintenant, donne-moi la réponse que tu as reçue.", style="bold blue"
        )
        reponse_user = Prompt.ask("[cyan]Quelle a été la réponse à analyser ?[/cyan]")

        with console.status(
            "[bold green]Analyse en cours... L'esprit de Cynic s'éveille...[/bold green]"
        ):
            analyzer = CynicAnalyzer(api_key=api_key)
            analyse = analyzer.analyze(contexte=contexte_user, reponse=reponse_user)
            sleep(1)

        # Rapport d'analyse de Mistral
        console.print("\n[bold]--- RAPPORT D'ANALYSE DE CYNIC ---[/bold]")
        score_final = analyse.get("score", -1)
        verdict_final = analyse.get("verdict", "Aucun verdict reçu.")
        couleur_style = "green"
        if score_final > 7:
            couleur_style = "bold red"
        elif score_final > 4:
            couleur_style = "yellow"
        console.print(
            f"\nScore de cynisme estimé : [{couleur_style}]{score_final} / 10[/{couleur_style}]"
        )
        console.print(Panel(Text(verdict_final, justify="center"), style=couleur_style))

    except KeyboardInterrupt:
        console.print(
            "\n\n[bold yellow]Interruption détectée.[/bold yellow] Cynic vous salue bien."
        )


if __name__ == "__main__":
    main()
