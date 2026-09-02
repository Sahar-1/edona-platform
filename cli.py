import typer
import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

app = typer.Typer()
console = Console()

API_BASE_URL = "http://localhost:8000"

@app.command()
def health():
    """
    Vérifie la santé de l'API FastAPI EDONA.
    """
    try:
        # L'endpoint /health correspond exactement à celui défini dans main.py
        response = requests.get(f"{API_BASE_URL}/health")
        response.raise_for_status()
        data = response.json()
        panel = Panel(
            f"[bold green]{data.get('status', 'unknown').upper()}[/bold green]\n{data.get('message', '')}",
            title="EDONA API Santé",
            style="bold green" if data.get('status') == "ok" else "bold red",
            box=box.ROUNDED
        )
        console.print(panel)
    except requests.RequestException as exc:
        panel = Panel(
            f"[bold red]Échec de connexion à l'API : {exc}[/bold red]",
            title="EDONA API Santé",
            style="bold red",
            box=box.ROUNDED
        )
        console.print(panel)

@app.command()
def list_items():
    """
    Affiche la liste des objets depuis l'API EDONA dans un tableau.
    """
    try:
        # Met à jour ici si jamais l'endpoint n'était pas correct.
        # L'API utilise bien /api/v1/items pour la liste (correspond à main.py).
        response = requests.get(f"{API_BASE_URL}/api/v1/items")
        response.raise_for_status()
        items = response.json()
        table = Table(title="Objets EDONA", box=box.ROUNDED)
        table.add_column("ID", justify="center", style="cyan")
        table.add_column("Titre", justify="left", style="magenta")
        table.add_column("Statut", justify="center", style="green")
        table.add_column("URL Image", justify="left", style="yellow")
        if not items:
            console.print("[i yellow]Aucun objet trouvé.[/i yellow]")
        else:
            for item in items:
                table.add_row(
                    str(item.get("id", "")),
                    item.get("title", ""),
                    str(item.get("status", "")),
                    item.get("image_url", ""),
                )
            console.print(table)
    except requests.RequestException as exc:
        console.print(f"[bold red]Erreur lors de la récupération des objets: {exc}[/bold red]")

if __name__ == "__main__":
    app()