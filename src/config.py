import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")


def _require(key: str) -> str:
    value = os.getenv(key, "").strip()
    if not value:
        print(f"\nERRO: Variável '{key}' não encontrada no .env\n", file=sys.stderr)
        sys.exit(1)
    return value


ANTHROPIC_API_KEY: str = _require("ANTHROPIC_API_KEY")
LLM_MODEL: str = os.getenv("LLM_MODEL", "claude-haiku-4-5")
MAX_TOPIC_LENGTH: int = int(os.getenv("MAX_TOPIC_LENGTH", "300"))

# Redes sociais suportadas
SUPPORTED_NETWORKS = {"instagram", "linkedin", "twitter"}

# Tons de voz disponíveis
SUPPORTED_TONES = {"profissional", "descontraido", "inspiracional", "educativo"}

# Limites de caracteres por rede
CHAR_LIMITS = {
    "instagram": 2200,
    "linkedin": 3000,
    "twitter": 280,  # por tweet individual na thread
}