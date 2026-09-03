"""Compatibilidade temporária com importações antigas.

O código novo deve usar filmes_projetc.services diretamente.
"""

from django.shortcuts import get_object_or_404

from filmes_projetc.models import Filmes, MagnetcLinks, link_series
from filmes_projetc.services.catalogo import (
    FilmeDuplicadoError,
    cadastrar_filme,
    editar_filme,
)
from filmes_projetc.services.tmdb import TMDBError


class ChamaDB:
    filme = Filmes
    links = MagnetcLinks
    serieDB = link_series


class CadastrarFilme:
    def __init__(self, nome, genero, link):
        self.nome = nome
        self.genero = genero
        self.link = link

    def verifica(self):
        try:
            cadastrar_filme(
                self.nome,
                self.genero,
                {"link_1080p_dub": self.link or ""},
            )
        except (FilmeDuplicadoError, TMDBError) as erro:
            return str(erro)
        return "Filme criado com sucesso."


class Editar_filme_criado:
    def __init__(self, id, nome, genero, link):
        self.id = id
        self.nome = nome
        self.genero = genero
        self.link = link

    def confirm(self):
        filme = get_object_or_404(Filmes, id=self.id)
        editar_filme(
            filme,
            self.nome or filme.nome,
            self.genero or filme.genero,
            {"link_1080p_dub": self.link or ""},
        )


class Editar_filme_serie_criado(Editar_filme_criado):
    def __init__(self, id, nome, genero):
        super().__init__(id, nome, genero, "")

    def cadastra_ep(self, ep_name, linkEp):
        link_series.objects.create(id_vinculado_id=self.id, ep_name=ep_name, link_eps=linkEp)

    def editaEP(self, ep_name, linkEp, id):
        episodio = get_object_or_404(link_series, id_vinculado_id=id, ep_name=ep_name)
        episodio.link_eps = linkEp
        episodio.save(update_fields=("link_eps",))


class Excluir_filme_db:
    def __init__(self, id):
        self.id = id

    def confirm(self):
        get_object_or_404(Filmes, id=self.id).delete()

    confirm_exclui_serie = confirm

    def excluir_ep_es(self, nome_ep):
        get_object_or_404(link_series, id_vinculado_id=self.id, ep_name=nome_ep).delete()


class Abas_Genero:
    def __init__(self, genero):
        self.genero = genero

    def retorno(self):
        return Filmes.objects.filter(genero=self.genero)
