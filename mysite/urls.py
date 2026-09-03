from django.contrib import admin
from django.urls import path

from filmes_projetc.views import (
    Abas,
    Cadastrar_filme,
    Editar_filme,
    Excluir,
    Filme,
    Home,
    Pesquisa,
    Propaganda,
)


urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("pesquisa/", Pesquisa.as_view(), name="pesquisa"),
    path("filme/<int:id>/", Filme.as_view(), name="filme"),
    path("cadastrar_filme/", Cadastrar_filme.as_view(), name="cadastrar_filme"),
    path("excluir/<int:id>/", Excluir.as_view(), name="excluir"),
    path("editar_filme/<int:id>/", Editar_filme.as_view(), name="editar_filme"),
    path("propaganda/<int:id>/", Propaganda.as_view(), name="propaganda"),
    path("abas/<str:genero0>/", Abas.as_view(), name="abas"),
    path("entradachefe/", admin.site.urls),
]
