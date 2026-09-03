from unittest.mock import Mock

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .models import Filmes, MagnetcLinks, link_series
from .services.catalogo import cadastrar_filme
from .services.tmdb import TMDBClient


class TMDBClientTests(TestCase):
    @override_settings(TMDB_API_KEY="teste")
    def test_serie_usa_endpoint_tv(self):
        resposta = Mock()
        resposta.raise_for_status.return_value = None
        resposta.json.return_value = {
            "results": [{"id": 1, "name": "Série", "first_air_date": "2026-01-01"}]
        }
        sessao = Mock()
        sessao.get.return_value = resposta

        TMDBClient(session=sessao).buscar_primeiro("Série", "serie")

        self.assertIn("/search/tv", sessao.get.call_args.args[0])


class CatalogoTests(TestCase):
    def test_cadastro_cria_filme_e_links_juntos(self):
        cliente = Mock()
        cliente.buscar_primeiro.return_value = {
            "tmdb_id": 10,
            "nome": "Filme",
            "tamb": "/poster.jpg",
            "sinopse": "Sinopse",
            "data_filme": "2026-01-01",
        }
        filme = cadastrar_filme(
            "Filme",
            "filme",
            {"link_1080p_dub": "magnet:?xt=teste"},
            tmdb_client=cliente,
        )
        self.assertEqual(filme.links_download.link_1080p_dub, "magnet:?xt=teste")

    def test_exclusao_em_cascata(self):
        serie = Filmes.objects.create(nome="Série", genero="serie")
        MagnetcLinks.objects.create(id=serie)
        link_series.objects.create(id_vinculado=serie, ep_name="E01", link_eps="link")
        serie.delete()
        self.assertFalse(MagnetcLinks.objects.exists())
        self.assertFalse(link_series.objects.exists())


class PermissaoTests(TestCase):
    def test_usuario_comum_nao_abre_cadastro(self):
        usuario = get_user_model().objects.create_user("usuario", password="senha-forte")
        self.client.force_login(usuario)
        resposta = self.client.get(reverse("cadastrar_filme"))
        self.assertEqual(resposta.status_code, 403)


class CatalogoViewTests(TestCase):
    def setUp(self):
        self.antigo = Filmes.objects.create(
            nome="Aventura antiga",
            genero="filme",
            sinopse="Uma jornada no espaço",
        )
        self.recente = Filmes.objects.create(
            nome="Série recente",
            genero="serie",
            sinopse="Investigação futurista",
        )

    def test_mais_recentemente_alterado_aparece_primeiro(self):
        Filmes.objects.filter(pk=self.antigo.pk).update(atualizado_em=timezone.now())
        resposta = self.client.get(reverse("home"))
        itens = list(resposta.context["filme"])
        self.assertEqual(itens[0].pk, self.antigo.pk)

    def test_pesquisa_por_varias_palavras_e_sinopse(self):
        resposta = self.client.get(reverse("home"), {"pesquisa": "jornada espaço"})
        self.assertContains(resposta, "Aventura antiga")
        self.assertNotContains(resposta, "Série recente")

    def test_pesquisa_ajax_retorna_apenas_resultados(self):
        resposta = self.client.get(
            reverse("home"),
            {"pesquisa": "Série"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertTemplateUsed(resposta, "components/catalogo_resultados.html")
        self.assertContains(resposta, 'id="catalogo-resultados"')
        self.assertNotContains(resposta, "<html")
