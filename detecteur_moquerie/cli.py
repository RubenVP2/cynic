from time import sleep
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
from rich.syntax import Syntax
from .analyzer import analyser_reponse_avec_mistral  # On importe notre analyseur
from .prompts import PROMPT_SYSTEME  # On importe aussi le prompt pour l'afficher


def main():
    """
    Fonction principale qui gère l'application.
    """
    console = Console()

    titre = Panel(
        Text(
            "🕵️‍♂️ Le Détecteur de Moquerie 2.0 (Powered by Mistral) 🕵️‍♀️",
            justify="center",
            style="bold magenta",
        ),
        title="[bold cyan]Bienvenue[/bold cyan]",
        subtitle="[bold cyan]Une IA pour enfin savoir si on vous prend pour un(e) idiot(e)[/bold cyan]",
    )
    console.print(titre)

    # On affiche le prompt système pour que l'utilisateur sache comment l'IA est briefée
    console.print(
        Panel(
            Syntax(PROMPT_SYSTEME, "markdown", theme="dracula", word_wrap=True),
            title="[bold yellow]Instruction donnée à l'IA[/bold yellow]",
        )
    )

    console.print("\nPour commencer, décris la situation.", style="bold blue")
    contexte_user = Prompt.ask(
        "[cyan]Quel était le message ou la question d'origine ?[/cyan]"
    )

    console.print(
        "\nMaintenant, donne-moi la réponse que tu as reçue.", style="bold blue"
    )
    reponse_user = Prompt.ask("[cyan]Quelle a été la réponse à analyser ?[/cyan]")

    with console.status(
        "[bold green]Analyse en cours... Connexion à l'intelligence suprême de Mistral...[/bold green]"
    ):
        sleep(1)  # Petite pause pour le style
        analyse = analyser_reponse_avec_mistral(contexte_user, reponse_user)
        sleep(1)

    console.print("\n[bold]--- RAPPORT D'ANALYSE DE MISTRAL ---[/bold]")

    score_final = analyse.get("score", -1)
    verdict_final = analyse.get("verdict", "Aucun verdict reçu.")

    # On choisit la couleur en fonction du score
    couleur_style = "green"
    if score_final > 7:
        couleur_style = "bold red"
    elif score_final > 4:
        couleur_style = "yellow"

    console.print(
        f"\nScore de moquerie estimé : [{couleur_style}]{score_final} / 10[/{couleur_style}]"
    )
    console.print(Panel(Text(verdict_final, justify="center"), style=couleur_style))


if __name__ == "__main__":
    main()
