"""
Persiste posts aprovados em JSON.

O formato JSON facilita integração futura com:
- Buffer API (agendamento de posts)
- Hootsuite
- n8n (automação de publicação)
- Make (Integromat)
"""
import json
import logging
from datetime import datetime
from pathlib import Path

from generator import GeneratedPost

logger = logging.getLogger(__name__)

POSTS_DIR = Path("posts")


def save_approved_posts(posts: list[GeneratedPost], topic: str) -> str | None:
    """
    Salva os posts aprovados em um arquivo JSON.

    Args:
        posts: Lista de posts (aprovados e rejeitados).
        topic: Tema original dos posts.

    Returns:
        Caminho do arquivo salvo, ou None se nenhum aprovado.
    """
    approved = [p for p in posts if p.approved]

    if not approved:
        logger.info("Nenhum post aprovado para salvar.")
        return None

    POSTS_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    topic_slug = topic[:30].lower().replace(" ", "_").replace("/", "-")
    filename = f"{timestamp}_{topic_slug}.json"
    filepath = POSTS_DIR / filename

    data = {
        "generated_at": datetime.now().isoformat(),
        "topic": topic,
        "total_generated": len(posts),
        "total_approved": len(approved),
        "posts": [
            {
                "network": p.network,
                "tone": p.tone,
                "content": p.final_content,
                "char_count": len(p.final_content),
                "was_edited": bool(p.edited_content),
                "approved_at": datetime.now().isoformat(),
            }
            for p in approved
        ],
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    logger.info("Posts salvos: %s (%d aprovados)", filepath, len(approved))
    return str(filepath)


def list_saved_posts() -> list[dict]:
    """Lista todos os posts salvos."""
    if not POSTS_DIR.exists():
        return []

    posts = []
    for filepath in sorted(POSTS_DIR.glob("*.json"), reverse=True):
        try:
            with open(filepath, encoding="utf-8") as f:
                data = json.load(f)
            posts.append({
                "file": filepath.name,
                "topic": data.get("topic", ""),
                "generated_at": data.get("generated_at", ""),
                "total_approved": data.get("total_approved", 0),
            })
        except Exception:
            continue

    return posts