import os
os.environ.setdefault("ANTHROPIC_API_KEY", "sk-ant-test-fake")

from unittest.mock import MagicMock, patch
import pytest


class TestGenerator:

    @patch("generator._client")
    def test_gera_post_instagram(self, mock_client):
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Post sobre liderança 🚀 #NexusConsultoria #Gestão")]
        mock_client.messages.create.return_value = mock_response

        from generator import generate_post
        post = generate_post("Liderança empresarial", "instagram", "profissional")

        assert post.network == "instagram"
        assert post.topic == "Liderança empresarial"
        assert post.tone == "profissional"
        assert len(post.content) > 0
        assert post.approved is False

    @patch("generator._client")
    def test_gera_post_linkedin(self, mock_client):
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Artigo sobre gestão de equipes remotas...")]
        mock_client.messages.create.return_value = mock_response

        from generator import generate_post
        post = generate_post("Gestão remota", "linkedin", "educativo")

        assert post.network == "linkedin"
        assert post.char_count > 0

    @patch("generator._client")
    def test_gera_todos_os_posts(self, mock_client):
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Conteúdo gerado")]
        mock_client.messages.create.return_value = mock_response

        from generator import generate_all
        posts = generate_all(
            "Transformação digital",
            ["instagram", "linkedin", "twitter"],
            "inspiracional",
        )

        assert len(posts) == 3
        assert {p.network for p in posts} == {"instagram", "linkedin", "twitter"}

    @patch("generator._client")
    def test_erro_na_geracao_retorna_post_com_erro(self, mock_client):
        mock_client.messages.create.side_effect = Exception("API error")

        from generator import generate_all
        posts = generate_all("Tema qualquer", ["instagram"], "profissional")

        assert len(posts) == 1
        assert "Erro" in posts[0].content

    def test_final_content_usa_edicao_se_disponivel(self):
        from generator import GeneratedPost
        post = GeneratedPost(
            network="instagram",
            topic="teste",
            tone="profissional",
            content="Conteúdo original",
            char_count=18,
        )
        post.edited_content = "Conteúdo editado"

        assert post.final_content == "Conteúdo editado"

    def test_final_content_usa_original_sem_edicao(self):
        from generator import GeneratedPost
        post = GeneratedPost(
            network="instagram",
            topic="teste",
            tone="profissional",
            content="Conteúdo original",
            char_count=18,
        )

        assert post.final_content == "Conteúdo original"