from static.js_py.Crud_filme import ChamaDB, Abas_Genero,Editar_filme_serie_criado
from static.js_py.Crud_filme import CadastrarFilme, Excluir_filme_db,Editar_filme_criado

from static.js_py.Pesquisa_filme import Pesquisa_nome_popular,Pesquisa_Genero
from static.js_py.tratamento_data import Tratamento_ep_name

from django.views.generic import View,ListView
from django.shortcuts import render

from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User


user = User.objects.get(id=1)

class Home(ListView):
    model = ChamaDB.filme
    template_name = 'home.html'
    context_object_name = 'filme'
    ordering = ['-id']
    paginate_by = 20

class Filme(View):

    def get(self, request, id):
        try:
            filme = ChamaDB.filme.objects.get(id=id)
            links = ChamaDB.links.objects.get(id=id)
            linksEP = ChamaDB.serieDB.objects.get(id_vinculado=id)

            if filme.genero == 'filme':
                return render(request, 'filme.html', {'filme': filme, 'links':links})
            else:
                nome = Tratamento_ep_name(linksEP).tra()
                return render(request, 'filme.html', {'filme': filme, 'links':links, "linksEP":linksEP, "nomeEp":nome})
        except:
            return render(request, 'filme.html', {'filme': filme, 'links':links})
            
    def post(self,request, id):
        try:
            filme = ChamaDB.filme.objects.get(id=id)
            links = ChamaDB.links.objects.get(id=id)
            linksEP = ChamaDB.serieDB.objects.filter(id_vinculado=id)
            if filme.genero == 'filme':
                return render(request, 'filme.html', {'filme': filme, 'links':links})
            else:
                nome = Tratamento_ep_name(linksEP).tra()
                return render(request, 'filme.html', {'filme': filme, 'links':links, "linksEP":linksEP, "nomeEp":nome})
        
        except: 
            raise
        
class Cadastrar_filme(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser
    
    def post(self,request):
        if request.user.is_superuser:
            if request.POST.get('nome'):
                a = CadastrarFilme(
                    nome=request.POST.get('nome'),
                    genero=request.POST.get('genero'),
                    link=request.POST.get('link')
                )
                return render(request, 'cadastrar_filme.html', {'mensagem': a.verifica()}) 
        
            if request.POST.get('pesquisa'):
                pes = Pesquisa_nome_popular(request.POST.get('pesquisa'))
                return render(request, 'cadastrar_filme.html', {'pesquisa': pes.retorno()})   
                
    def get(self,request):
        return render(request, 'cadastrar_filme.html')                                                                           

class Excluir(UserPassesTestMixin, View):
    template_name = 'pesquisa.html'
    def test_func(self):
        return self.request.user.is_superuser
    
    if user.is_superuser:
        def post(self,request, id):
            if ChamaDB.filme.objects.get(id=id).genero == "serie":
                Excluir_filme_db(id=id).confirm_exclui_serie()
                return render(request, 'home.html')
            if ChamaDB.filme.objects.get(id=id).genero == "filme":
                Excluir_filme_db(id=id).confirm()
                return render(request, 'home.html')

class Editar_filme(View):
    def post(self,request,id):
        if request.user.is_superuser:
            if ChamaDB.filme.objects.get(id=id).genero == "filme":
                Editar_filme_criado(
                    id=id,
                    nome=request.POST.get('nome'),
                    genero=request.POST.get('genero'),
                    link=request.POST.get('link')
                                    ).confirm()
                
            if ChamaDB.filme.objects.get(id=id).genero == "serie":
                editir = Editar_filme_serie_criado(id=id, nome=request.POST.get("nome"),genero=request.POST.get("genero"))
                editir.confirm()
                acao = request.POST.get('criar_editar_excluir')
                if acao == "criar":
                    editir.confirm()
                    editir.cadastra_ep(ep_name=request.POST.get('nomeEP'), linkEp=request.POST.get('linksEP'))

                if acao == "editar":
                    editir.editaEP(id=id, ep_name=request.POST.get('nomeEP'), linkEp=request.POST.get('linksEP'))

                if acao == "excluir":
                    a = Excluir_filme_db(id=id)
                    a.excluir_ep_es(nome_ep=request.POST.get('nomeEP'))
                

        else:
            raise TypeError("erro no super user ou pegada do banco de dados/ post/ editar_filme")

class Pesquisa(View):
    def post(self,request):
        pes = Pesquisa_Genero(request.POST.get('pesquisa'))
        if pes.retorno():
            return render(request, 'pesquisa.html', {'resultado': pes.retorno()})
        else:
            return render(request, 'pesquisa.html')
        
class Abas(View):
    def post(self,request,genero0):
        filmes = Abas_Genero(genero0).retorno()
        return render(request, 'abas.html', {'resultado': filmes})

class Propaganda(View):
    def get(self,request,id):
        link = ChamaDB.links.objects.get(id=id)
        return render(request, 'propaganda.html', {'link': link})
