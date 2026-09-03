import requests
from django.conf import settings


class TMDBError(Exception):
    """Erro seguro para ser exibido ao administrador."""


class TMDBClient:
    BASE_URL = "https://api.themoviedb.org/3"

    def __init__(self, api_key=None, session=None):
        self.api_key = api_key or settings.TMDB_API_KEY
        self.session = session or requests.Session()

    def buscar_primeiro(self, nome, tipo):
        if not self.api_key:
            raise TMDBError("Configure a variável TMDB_API_KEY.")

        endpoint = "tv" if tipo == "serie" else "movie"
        try:
            resposta = self.session.get(
                f"{self.BASE_URL}/search/{endpoint}",
                params={
                    "api_key": self.api_key,
                    "language": "pt-BR",
                    "query": nome,
                },
                timeout=10,
            )
            resposta.raise_for_status()
            resultados = resposta.json().get("results", [])
        except (requests.RequestException, ValueError) as erro:
            raise TMDBError("Não foi possível consultar o TMDB agora.") from erro

        if not resultados:
            raise TMDBError("Nenhum resultado foi encontrado no TMDB.")

        item = resultados[0]
        return {
            "tmdb_id": item["id"],
            "nome": item.get("title") or item.get("name") or nome,
            "tamb": item.get("poster_path") or "",
            "sinopse": item.get("overview") or "",
            "data_filme": item.get("release_date")
            or item.get("first_air_date")
            or "",
        }
