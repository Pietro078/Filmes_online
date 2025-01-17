import requests

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

SECRETKEY = '17528cca6d733031cd27a0916ee4cde5'

from filmes_projetc.models import Filmes, MagnetcLinks
user = User.objects.get(id=1)

def home(request):
    #Filmes.objects.all().order_by('-id')
    if request.method=='GET':
        filme=Filmes.objects.all().order_by('-id')
        paginator = Paginator(filme, 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        ff = 'filme'
        ss = 'serie'
        return render(request, 'home.html', {'filme': page_obj, 'page_obj':page_obj, 'ff':ff, 'ss':ss})
    
    

    
                    
    return render(request, 'home.html', {'filme': page_obj, 'page_obj':page_obj, 'ff':ff, 'ss':ss})

def filme(request, id):
    if request.method == 'GET':
        filme = Filmes.objects.get(id=id)
        links = MagnetcLinks.objects.get(id=id)

        return render(request, 'filme.html', {'filme': filme, 'links':links})
    
    if request.method == 'POST':  
        filme = Filmes.objects.get(id=id)
        links = MagnetcLinks.objects.get(id=id)

        return render(request, 'filme.html', {'filme': filme, 'links':links})

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def cadastrar_filme(request):
    
    if request.user.is_superuser and request.method == 'POST':

        nome = request.POST.get('nome')
        genero = request.POST.get('genero')
        link = request.POST.get('link')
        
        pesquisa = request.POST.get('pesquisa')

        if pesquisa:

            busca = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={SECRETKEY}&language=pt-BR&query={pesquisa}")
            busca = busca.json()
            busca = busca['results']
            for a in busca:
                return render(request, 'cadastrar_filme.html', {'pesquisa': a['title']})
        if user.is_superuser:
            if nome:
                # Busca o filme na API do TMDB pelo nome
                busca = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={SECRETKEY}&language=pt-BR&query={nome}")
                busca = busca.json()

                try:
                # Verifica se já existe um filme com o mesmo nome
                    Filmes.objects.get(nome=nome)
                    mensagem = 'Filme já existe e não pode ser criado novamente.'
                    return render(request, 'cadastrar_filme.html', {'mensagem': mensagem})
                except ObjectDoesNotExist:
                    if 'results' in busca and busca['results']:
                        n = 0
                        
                        for a in busca['results']:
                            while n < 1: 
                                filme = Filmes.objects.create(
                                    nome=a['title'],
                                    genero=genero,  
                                    tamb=a['poster_path'],
                                    sinopse=a['overview'],
                                    data_filme=a['release_date']
                                )
                                
                                MagnetcLinks.objects.create(
                                    link_1080p_dub=link,
                                    id=filme.id  
                                )
                                n+=1
                                
            mensagem = 'filme criado com sucesso'
            return render(request, 'cadastrar_filme.html', {'mensagem': mensagem}) 
    
    if request.method== 'GET':
        return render(request, 'cadastrar_filme.html')
    
@user_passes_test(is_admin)
def excluir(request, id):
    if user.is_superuser:
        filme = get_object_or_404(Filmes, id=id)
        link = get_object_or_404(MagnetcLinks, id=id)

        if request.method == 'POST':
            filme.delete()
            link.delete()

            return render(request, 'home.html', {'id':id})

def editar_filme(request, id):
    filme = get_object_or_404(Filmes, id=id)
    link = get_object_or_404(MagnetcLinks, id=id)     

    if request.user.is_superuser and request.method == 'POST':
        nome = request.POST.get('nome')
        genero = request.POST.get('genero')
        link = request.POST.get('link')

        if not nome:
            nome = filme.nome
        if not genero:
            genero = filme.genero
        if not link:
            link = MagnetcLinks.link_1080p_dub
        
        if nome:
            busca = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={SECRETKEY}&language=pt-BR&query={nome}")
            busca = busca.json()
        if user.is_superuser:
            n=0
            if 'results' in busca and busca['results']:  
                for a in busca['results']:
                    while n < 1:

                        filme.nome = a['title']
                        filme.genero = genero
                        filme.tamb = a['poster_path']
                        filme.data_filme = a['release_date']
                        filme.sinopse = a['overview']

                        link.link = link

                        filme.save()
                        link.save()
                        n+=1

def pesquisa(request):

    if request.method == 'POST':
        pesquisa = request.POST.get('pesquisa')
        resultados =[]
        if pesquisa:
                resultados = Filmes.objects.filter(nome__icontains=pesquisa)
                return render(request, 'pesquisa.html', {'resultado': resultados})
        else:
            return render(request, 'pesquisa.html')


def abas(request, genero0):

    btnfilme = request.POST.get('btnfilme') 
    btnserie = request.POST.get('btnserie') 
    if request.method == 'POST':
        filmes = []
        
        if genero0=='filme':
            filmes = (Filmes.objects.filter(genero=genero0))
            return render(request, 'abas.html', {'resultado': filmes})
        
        if genero0=='serie':
            filmes = Filmes.objects.filter(genero=genero0)
            return render(request, 'abas.html', {'resultado': filmes})
    else:
        return render(request, 'pesquisa.html')

def propaganda(request, id):
    link = MagnetcLinks.objects.get(id=id)

    return render(request, 'propaganda.html', {'link': link})
