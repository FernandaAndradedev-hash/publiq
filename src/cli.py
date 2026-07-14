"""
Interface CLI do ContentFlow com Rich.
"""
import logging
import sys

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich import box

from generator import generate_all
from reviewer import review_all
from storage import list_saved_posts, save_approved_posts
from validators import validate_network, validate_tone, validate_topic

logging.basicConfig(level=logging.WARNING)
console = Console()


def print_banner():
    console.print(Panel.fit(
        "[bold cyan]ContentFlow[/bold cyan]\n"
        "[dim]Gerador de conteúdo para redes sociais — Nexus Consultoria[/dim]",
        border_style="cyan",
    ))


def select_networks() -> list[str]:
    """Solicita ao usuário quais redes sociais usar."""
    console.print("\n[bold]Redes sociais disponíveis:[/bold]")
    console.print("  [magenta]1[/magenta] — Instagram")
    console.print("  [blue]2[/blue] — LinkedIn")
    console.print("  [cyan]3[/cyan] — Twitter/X")
    console.print("  [green]4[/green] — Todas\n")

    choice = Prompt.ask("Escolha as redes (ex: 1,2 ou 4)", default="4")

    mapping = {
        "1": ["instagram"],
        "2": ["linkedin"],
        "3": ["twitter"],
        "4": ["instagram", "linkedin", "twitter"],
    }

    # Permite múltipla seleção: "1,2"
    networks = []
    for part in choice.split(","):
        part = part.strip()
        if part in mapping:
            networks.extend(mapping[part])

    # Remove duplicatas mantendo ordem
    seen = set()
    unique = []
    for n in networks:
        if n not in seen:
            seen.add(n)
            unique.append(n)

    return unique if unique else ["instagram", "linkedin", "twitter"]


def select_tone() -> str:
    """Solicita o tom de voz."""
    console.print("\n[bold]Tom de voz:[/bold]")
    console.print("  1 — Profissional")
    console.print("  2 — Descontraído")
    console.print("  3 — Inspiracional")
    console.print("  4 — Educativo\n")

    tone_map = {
        "1": "profissional",
        "2": "descontraido",
        "3": "inspiracional",
        "4": "educativo",
    }

    choice = Prompt.ask("Escolha o tom", choices=["1", "2", "3", "4"], default="1")
    return tone_map[choice]


def show_saved_posts():
    """Exibe lista de posts salvos."""
    posts = list_saved_posts()

    if not posts:
        console.print("[dim]Nenhum post salvo ainda.[/dim]")
        return

    table = Table(title="Posts Salvos", box=box.ROUNDED)
    table.add_column("Arquivo", style="dim")
    table.add_column("Tema")
    table.add_column("Gerado em")
    table.add_column("Aprovados", justify="center")

    for p in posts[:10]:  # últimos 10
        table.add_row(
            p["file"],
            p["topic"][:40] + ("..." if len(p["topic"]) > 40 else ""),
            p["generated_at"][:19].replace("T", " "),
            str(p["total_approved"]),
        )

    console.print(table)


def main():
    print_banner()

    # Modo listagem
    if "--list" in sys.argv:
        show_saved_posts()
        return

    console.print("\n[dim]Pressione Ctrl+C a qualquer momento para sair.[/dim]\n")

    try:
        # 1. Tema
        topic_raw = Prompt.ask("[bold]Tema do post[/bold]")
        try:
            topic = validate_topic(topic_raw)
        except (ValueError, TypeError) as exc:
            console.print(f"[red]Tema inválido:[/red] {exc}")
            return

        # 2. Redes sociais
        networks = select_networks()
        validated_networks = []
        for n in networks:
            try:
                validated_networks.append(validate_network(n))
            except ValueError:
                pass

        if not validated_networks:
            console.print("[red]Nenhuma rede válida selecionada.[/red]")
            return

        # 3. Tom de voz
        tone_raw = select_tone()
        try:
            tone = validate_tone(tone_raw)
        except ValueError as exc:
            console.print(f"[red]{exc}[/red]")
            return

        # 4. Geração
        console.print(f"\n[dim]Gerando posts para: {', '.join(validated_networks)}...[/dim]\n")
        posts = generate_all(topic, validated_networks, tone)

        # 5. Revisão humana
        console.print("\n[bold cyan]─── Revisão de Posts ───[/bold cyan]\n")
        reviewed = review_all(posts)

        # 6. Salvar aprovados
        filepath = save_approved_posts(reviewed, topic)

        # 7. Resumo final
        approved_count = sum(1 for p in reviewed if p.approved)
        console.print(Panel(
            f"[bold]Total gerado:[/bold] {len(posts)}\n"
            f"[bold green]Aprovados:[/bold green] {approved_count}\n"
            f"[bold red]Rejeitados:[/bold red] {len(posts) - approved_count}\n"
            + (f"[bold]Arquivo:[/bold] {filepath}" if filepath else ""),
            title="📊 Resumo",
            border_style="green",
        ))

    except KeyboardInterrupt:
        console.print("\n[dim]Encerrando ContentFlow.[/dim]")


if __name__ == "__main__":
    main()