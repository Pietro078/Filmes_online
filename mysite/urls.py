from django.contrib import admin
from django.urls import path, include
from filmes_projetc.views import home, filme, cadastrar_filme, pesquisa, excluir, editar_filme, propaganda, abas


urlpatterns = [
    path('pesquisa/', pesquisa, name='pesquisa'),
    path('filme/<int:id>', filme, name='filme'),
    path('cadastrar_filme/', cadastrar_filme, name='cadastrar_filme'),
    path('excluir/<int:id>', excluir, name='excluir'),
    path('editar_filme/<int:id>', editar_filme, name='editar_filme'),
    path('entradachefe/', admin.site.urls),
    path('', home, name='home'),
    path('propaganda/<int:id>', propaganda, name='propaganda'),
    path('abas/<str:genero0>', abas, name='abas')
]
