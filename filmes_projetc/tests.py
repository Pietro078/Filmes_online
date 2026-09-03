from unittest.mock import Mock

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

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
