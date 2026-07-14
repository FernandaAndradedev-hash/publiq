"""
Fluxo de revisão humana dos posts gerados.

O revisor exibe cada post e aguarda a decisão:
- Aprovar → salva o post como está
- Editar → permite modificar o conteúdo antes de aprovar
- Rejeitar → descarta o post

Esta é a camada "human in the loop" do sistema.
"""
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich import box
from rich.table import Table

from generator import GeneratedPost

console = Console()

# Indicadores visuais por rede
NETWORK_STYLES = {
    "instagram": (" Instagram", "magenta"),
    "linkedin": (" LinkedIn", "blue"),
    "twitter": (" Twitter/X", "cyan"),
}

# Indicador de limite de caracteres
CHAR_LIMITS = {
    "instagram": 2200,
    "linkedin": 3000,
    "twitter": 280,
}


def _format_char_count(post: GeneratedPost) -> str:
    """Exibe contagem de caracteres com alerta se próximo do limite."""
    limit = CHAR_LIMITS.get(post.network, 0)
    if not limit or post.network == "twitter":
        return f"{post.char_count} chars"

    percentage = (post.char_count / limit) * 100

    if percentage > 90:
        return f"[red]{post.char_count}/{limit} chars ({percentage:.0f}%)[/red]"
    elif percentage > 75:
        return f"[yellow]{post.char_count}/{limit} chars ({percentage:.0f}%)[/yellow]"
    else:
        return f"[green]{post.char_count}/{limit} chars ({percentage:.0f}%)[/green]"


def review_post(post: GeneratedPost) -> GeneratedPost:
    """
    Exibe um post e solicita decisão do usuário.

    Args:
        post: Post gerado para revisão.

    Returns:
        Post atualizado com decisão (approved=True/False e edited_content se editado).
    """
    network_label, color = NETWORK_STYLES.get(post.network, (post.network, "white"))
    char_info = _format_char_count(post)

    # Exibe o post
    console.print(Panel(
        post.content,
        title=f"[bold {color}]{network_label}[/bold {color}]",
        subtitle=char_info,
        border_style=color,
        padding=(1, 2),
    ))

    # Menu de decisão
    console.print("\n[bold]O que deseja fazer com este post?[/bold]")
    console.print("  [green]A[/green] — Aprovar")
    console.print("  [yellow]E[/yellow] — Editar e aprovar")
    console.print("  [red]R[/red] — Rejeitar\n")

    while True:
        choice = Prompt.ask("Sua escolha", choices=["a", "e", "r", "A", "E", "R"]).lower()

        if choice == "a":
            post.approved = True
            console.print(f"[green]✅ Post aprovado![/green]\n")
            break

        elif choice == "e":
            console.print("\n[yellow]Digite o conteúdo editado (Enter em linha vazia para finalizar):[/yellow]")
            lines = []
            while True:
                line = input()
                if line == "" and lines and lines[-1] == "":
                    break
                lines.append(line)
            edited = "\n".join(lines[:-1] if lines and lines[-1] == "" else lines).strip()

            if edited:
                post.edited_content = edited
                post.approved = True
                console.print(f"[green]✅ Post editado e aprovado![/green]\n")
            else:
                console.print("[yellow]Nenhuma edição feita. Post rejeitado.[/yellow]\n")
            break

        elif choice == "r":
            post.approved = False
            console.print(f"[red]❌ Post rejeitado.[/red]\n")
            break

    return post


def review_all(posts: list[GeneratedPost]) -> list[GeneratedPost]:
    """
    Revisa todos os posts gerados, um por um.

    Args:
        posts: Lista de posts gerados.

    Returns:
        Lista de posts com decisões aplicadas.
    """
    reviewed = []

    for i, post in enumerate(posts, 1):
        console.print(f"\n[dim]── Post {i} de {len(posts)} ──[/dim]\n")

        if "[Erro" in post.content:
            console.print(f"[red]⚠️ Post com erro para {post.network} — pulando.[/red]\n")
            reviewed.append(post)
            continue

        reviewed_post = review_post(post)
        reviewed.append(reviewed_post)

    return reviewed