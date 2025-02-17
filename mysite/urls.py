from django.contrib import admin
from django.urls import path, include
from filmes_projetc.views import Home, Filme, Cadastrar_filme, Pesquisa, Excluir, Editar_filme, Propaganda, Abas


urlpatterns = [
    path('pesquisa/', Pesquisa.as_view(), name='pesquisa'),
    path('filme/<int:id>', Filme.as_view(), name='filme'),
    path('cadastrar_filme/', Cadastrar_filme.as_view(), name='cadastrar_filme'),
    path('excluir/<int:id>', Excluir.as_view(), name='excluir'),
    path('editar_filme/<int:id>', Editar_filme.as_view(), name='editar_filme'),
    path('entradachefe/', admin.site.urls),
    path('', Home.as_view(), name='home'),
    path('propaganda/<int:id>', Propaganda.as_view(), name='propaganda'),
    path('abas/<str:genero0>', Abas.as_view(), name='abas')
]
