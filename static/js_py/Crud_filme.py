from filmes_projetc.models import Filmes, MagnetcLinks,link_series
from django.shortcuts import get_object_or_404
import requests

mensagem = ["Filme já existe e não pode ser criado novamente.","filme criado com sucesso"]

class ChamaDB:
    filme = Filmes
    links = MagnetcLinks
    serieDB = link_series
    
class CadastrarFilme:
    def __init__(self,nome, genero,link ):
        self.__nome = nome
        self.__genero = genero
        self.__link = link
        self.__SECRETKEY = '17528cca6d733031cd27a0916ee4cde5'
    
    def verifica(self):
        busca = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={self.__SECRETKEY}&language=pt-BR&query={self.__nome}")
        busca = busca.json()

        if  ChamaDB.filme.objects.filter(nome=self.__nome).exists():
                return mensagem[0]
        else:
            if 'results' in busca and busca['results']:
                n = 0
                        
            for a in busca['results']:
                while n < 1: 
                    filme = Filmes.objects.create(
                        nome=a['title'],
                        genero=self.__genero,  
                        tamb=a['poster_path'],
                        sinopse=a['overview'],
                        data_filme=a['release_date']
                        )
                                
                    ChamaDB.links.objects.create(
                            link_1080p_dub=self.__link,
                            id=filme.id  
                    )
                    n+=1
                                
            return mensagem[1]


class Editar_filme_criado:
    def __init__(self, id,nome,genero,link):
        self.__id = id
        self.__nome=nome
        self.__genero=genero
        self.__link=link
        self.__SECRETKEY = '17528cca6d733031cd27a0916ee4cde5'
          
        self.__filme = get_object_or_404(ChamaDB.filme, id=self.__id)
        self.__magnetc = get_object_or_404(ChamaDB.links, id=self.__id) 

    def confirm(self):
        if not self.__nome:
            self.__nome = self.__filme.nome
        if not self.__genero:
            self.__genero = self.__filme.genero
        if not  self.__link:
            self.__link = self.__magnetc.link_1080p_dub
        
        if self.__nome:
            busca = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={self.__SECRETKEY}&language=pt-BR&query={self.__nome}")
            busca = busca.json()
            n=0
            if 'results' in busca and busca['results']:  
                for a in busca['results']:
                    while n < 1:

                        self.__filme.nome = a['title']
                        self.__filme.genero = self.__genero
                        self.__filme.tamb = a['poster_path']
                        self.__filme.data_filme = a['release_date']
                        self.__filme.sinopse = a['overview']

                        self.__magnetc.link = self.__link

                        self.__filme.save()
                        self.__magnetc.save()
                        n+=1

class Editar_filme_serie_criado:
    def __init__(self, id,nome,genero):
        self.__id = id
        self.__nome=nome
        self.__genero=genero
        self.__SECRETKEY = '17528cca6d733031cd27a0916ee4cde5'
        self.__filme = get_object_or_404(Filmes, id=self.__id)

    def confirm(self):
        if not self.__nome:
            self.__nome = self.__filme.nome
        if not self.__genero:
            self.__genero = self.__filme.genero
        
        if self.__nome:
            busca = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={self.__SECRETKEY}&language=pt-BR&query={self.__nome}")
            busca = busca.json()
            n=0
            if 'results' in busca and busca['results']:  
                for a in busca['results']:
                    while n < 1:

                        self.__filme.nome = a['title']
                        self.__filme.genero = self.__genero
                        self.__filme.tamb = a['poster_path']
                        self.__filme.data_filme = a['release_date']
                        self.__filme.sinopse = a['overview']
                        self.__filme.save()
                        n+=1
        

    def cadastra_ep(self, ep_name, linkEp ):
        try:
            ChamaDB.serieDB.objects.create(
                ep_name = ep_name,
                link_eps=linkEp,
                id_vinculado=self.__id  
            )
        except:
            raise 

    def editaEP(self, ep_name, linkEp, id):
        ep = ChamaDB.serieDB.objects.get(id_vinculado=id, ep_name = ep_name)
        ep.link_eps = linkEp
        ep.save()
        
class Excluir_filme_db:
    def __init__(self,id):
          self.__id = id

    def confirm(self):
        get_object_or_404(ChamaDB.filme, id=self.__id).delete()
        get_object_or_404(ChamaDB.links, id=self.__id).delete()

    def confirm_exclui_serie(self):
        get_object_or_404(Filmes, id=self.__id).delete()
        ChamaDB.serieDB.objects.filter(id_vinculado=self.__id).delete()

    def excluir_ep_es(self, nome_ep):
        ep=ChamaDB.serieDB.objects.filter(id_vinculado=self.__id)
        ep.get(ep_name=nome_ep).delete()

class Abas_Genero:
    def __init__(self, genero):
        self.__genero0 = genero
        
    filmes = []
    def retorno(self):
        if self.__genero0 =='filme':
            filmes = (ChamaDB.filme.objects.filter(genero=self.__genero0))
            return filmes
            
        if self.__genero0=='serie':
            filmes = ChamaDB.filme.objects.filter(genero=self.__genero0)
            return filmes
