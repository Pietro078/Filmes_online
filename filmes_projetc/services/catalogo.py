from django.db import IntegrityError, transaction

from ..models import Filmes, MagnetcLinks
from .tmdb import TMDBClient


class FilmeDuplicadoError(Exception):
    pass


@transaction.atomic
def cadastrar_filme(nome, genero, links, tmdb_client=None):
    cliente = tmdb_client or TMDBClient()
    dados = cliente.buscar_primeiro(nome, genero)

    if Filmes.objects.filter(tmdb_id=dados["tmdb_id"], genero=genero).exists():
        raise FilmeDuplicadoError("Esse título já está cadastrado.")

    try:
        filme = Filmes.objects.create(genero=genero, **dados)
    except IntegrityError as erro:
        raise FilmeDuplicadoError("Esse título já está cadastrado.") from erro

    MagnetcLinks.objects.create(id=filme, **links)
    return filme


@transaction.atomic
def editar_filme(filme, nome, genero, links, tmdb_client=None):
    if nome != filme.nome or genero != filme.genero:
        cliente = tmdb_client or TMDBClient()
        dados = cliente.buscar_primeiro(nome, genero)
        duplicado = Filmes.objects.filter(
            tmdb_id=dados["tmdb_id"], genero=genero
        ).exclude(pk=filme.pk)
        if duplicado.exists():
            raise FilmeDuplicadoError("Esse título já está cadastrado.")
        for campo, valor in dados.items():
            setattr(filme, campo, valor)

    filme.genero = genero
    filme.save()
    MagnetcLinks.objects.update_or_create(id=filme, defaults=links)
    return filme
