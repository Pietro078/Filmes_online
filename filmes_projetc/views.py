from django.views.generic import View, ListView
from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404

from static.js_py.Crud_filme import (
    ChamaDB,
    Abas_Genero,
    Editar_filme_serie_criado,
    CadastrarFilme,
    Excluir_filme_db,
    Editar_filme_criado,
)

from static.js_py.Pesquisa_filme import (
    Pesquisa_nome_popular,
    Pesquisa_Genero,
)

from static.js_py.tratamento_data import Tratamento_ep_name


# =========================================================
# HOME
# =========================================================

class Home(ListView):

    model = ChamaDB.filme
    template_name = 'home.html'
    context_object_name = 'filme'
    ordering = ['-id']
    paginate_by = 20


# =========================================================
# FILME / SÉRIE
# =========================================================

class Filme(View):

    def get(self, request, id):

        try:
            filme = ChamaDB.filme.objects.get(id=id)

            links = ChamaDB.links.objects.get(id=id)

        except ChamaDB.filme.DoesNotExist:
            raise Http404("Filme não encontrado")

        except ChamaDB.links.DoesNotExist:
            return render(
                request,
                'filme.html',
                {
                    'filme': filme,
                }
            )

        context = {
            'filme': filme,
            'links': links,
        }

        if filme.genero != 'filme':

            linksEP = ChamaDB.serieDB.objects.filter(
                id_vinculado=id
            )

            nome = Tratamento_ep_name(
                linksEP
            ).tra()

            context.update({
                'linksEP': linksEP,
                'nomeEp': nome,
            })

        return render(
            request,
            'filme.html',
            context
        )

    def post(self, request, id):

        return self.get(
            request,
            id
        )


# =========================================================
# CADASTRAR FILME
# =========================================================

class Cadastrar_filme(UserPassesTestMixin, View):

    template_name = 'cadastrar_filme.html'

    def test_func(self):

        return self.request.user.is_superuser

    def get(self, request):

        return render(
            request,
            self.template_name
        )

    def post(self, request):

        # -------------------------------------------------
        # CADASTRAR FILME
        # -------------------------------------------------

        if request.POST.get('nome'):

            a = CadastrarFilme(

                nome=request.POST.get('nome'),

                genero=request.POST.get('genero'),

                link=request.POST.get('link')

            )

            return render(
                request,
                self.template_name,
                {
                    'mensagem': a.verifica()
                }
            )

        # -------------------------------------------------
        # PESQUISAR FILME
        # -------------------------------------------------

        if request.POST.get('pesquisa'):

            pes = Pesquisa_nome_popular(
                request.POST.get('pesquisa')
            )

            return render(
                request,
                self.template_name,
                {
                    'pesquisa': pes.retorno()
                }
            )

        return render(
            request,
            self.template_name
        )


# =========================================================
# EXCLUIR FILME
# =========================================================

class Excluir(UserPassesTestMixin, View):

    template_name = 'pesquisa.html'

    def test_func(self):

        return self.request.user.is_superuser

    def post(self, request, id):

        try:

            filme = ChamaDB.filme.objects.get(
                id=id
            )

        except ChamaDB.filme.DoesNotExist:

            raise Http404(
                "Filme não encontrado"
            )

        excluir = Excluir_filme_db(
            id=id
        )

        # -------------------------------------------------
        # EXCLUIR SÉRIE
        # -------------------------------------------------

        if filme.genero == "serie":

            excluir.confirm_exclui_serie()

        # -------------------------------------------------
        # EXCLUIR FILME
        # -------------------------------------------------

        elif filme.genero == "filme":

            excluir.confirm()

        return render(
            request,
            'home.html'
        )


# =========================================================
# EDITAR FILME / SÉRIE
# =========================================================

class Editar_filme(UserPassesTestMixin, View):

    def test_func(self):

        return self.request.user.is_superuser

    def post(self, request, id):

        try:

            filme = ChamaDB.filme.objects.get(
                id=id
            )

        except ChamaDB.filme.DoesNotExist:

            raise Http404(
                "Filme não encontrado"
            )

        # -------------------------------------------------
        # EDITAR FILME
        # -------------------------------------------------

        if filme.genero == "filme":

            editar = Editar_filme_criado(

                id=id,

                nome=request.POST.get('nome'),

                genero=request.POST.get('genero'),

                link=request.POST.get('link')

            )

            editar.confirm()

        # -------------------------------------------------
        # EDITAR SÉRIE
        # -------------------------------------------------

        elif filme.genero == "serie":

            editir = Editar_filme_serie_criado(

                id=id,

                nome=request.POST.get('nome'),

                genero=request.POST.get('genero')

            )

            # Atualiza os dados principais da série
            editir.confirm()

            acao = request.POST.get(
                'criar_editar_excluir'
            )

            # ---------------------------------------------
            # CRIAR EPISÓDIO
            # ---------------------------------------------

            if acao == "criar":

                editir.cadastra_ep(

                    ep_name=request.POST.get(
                        'nomeEP'
                    ),

                    linkEp=request.POST.get(
                        'linksEP'
                    )

                )

            # ---------------------------------------------
            # EDITAR EPISÓDIO
            # ---------------------------------------------

            elif acao == "editar":

                editir.editaEP(

                    id=id,

                    ep_name=request.POST.get(
                        'nomeEP'
                    ),

                    linkEp=request.POST.get(
                        'linksEP'
                    )

                )

            # ---------------------------------------------
            # EXCLUIR EPISÓDIO
            # ---------------------------------------------

            elif acao == "excluir":

                a = Excluir_filme_db(
                    id=id
                )

                a.excluir_ep_es(

                    nome_ep=request.POST.get(
                        'nomeEP'
                    )

                )

        return render(
            request,
            'filme.html',
            {
                'filme': filme
            }
        )


# =========================================================
# PESQUISA
# =========================================================

class Pesquisa(View):

    template_name = 'pesquisa.html'

    def post(self, request):

        pesquisa = request.POST.get(
            'pesquisa'
        )

        pes = Pesquisa_Genero(
            pesquisa
        )

        resultado = pes.retorno()

        if resultado:

            return render(
                request,
                self.template_name,
                {
                    'resultado': resultado
                }
            )

        return render(
            request,
            self.template_name
        )


# =========================================================
# ABAS DE GÊNERO
# =========================================================

class Abas(View):

    def post(self, request, genero0):

        filmes = Abas_Genero(
            genero0
        ).retorno()

        return render(
            request,
            'abas.html',
            {
                'resultado': filmes
            }
        )


# =========================================================
# PROPAGANDA
# =========================================================

class Propaganda(View):

    def get(self, request, id):

        try:

            link = ChamaDB.links.objects.get(
                id=id
            )

        except ChamaDB.links.DoesNotExist:

            raise Http404(
                "Link não encontrado"
            )

        return render(
            request,
            'propaganda.html',
            {
                'link': link
            }
        )