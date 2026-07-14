import os
os.environ.setdefault("ANTHROPIC_API_KEY", "sk-ant-test-fake")

import json
import pytest
from pathlib import Path
from generator import GeneratedPost


def make_post(network: str, approved: bool = True) -> GeneratedPost:
    post = GeneratedPost(
        network=network,
        topic="Liderança empresarial",
        tone="profissional",
        content=f"Post para {network} sobre liderança",
        char_count=30,
    )
    post.approved = approved
    return post


class TestStorage:

    def test_salva_posts_aprovados(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)

        from storage import save_approved_posts
        posts = [make_post("instagram"), make_post("linkedin")]
        filepath = save_approved_posts(posts, "Liderança empresarial")

        assert filepath is not None
        assert Path(filepath).exists()

        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)

        assert data["total_approved"] == 2
        assert len(data["posts"]) == 2

    def test_nao_salva_sem_aprovados(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)

        from storage import save_approved_posts
        posts = [make_post("instagram", approved=False)]
        filepath = save_approved_posts(posts, "Tema")

        assert filepath is None

    def test_salva_apenas_aprovados(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)

        from storage import save_approved_posts
        posts = [
            make_post("instagram", approved=True),
            make_post("linkedin", approved=False),
            make_post("twitter", approved=True),
        ]
        filepath = save_approved_posts(posts, "Tema")

        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)

        assert data["total_approved"] == 2
        networks = [p["network"] for p in data["posts"]]
        assert "instagram" in networks
        assert "twitter" in networks
        assert "linkedin" not in networks

    def test_lista_posts_salvos(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)

        from storage import save_approved_posts, list_saved_posts
        save_approved_posts([make_post("instagram")], "Tema 1")
        save_approved_posts([make_post("linkedin")], "Tema 2")

        posts = list_saved_posts()
        assert len(posts) == 2