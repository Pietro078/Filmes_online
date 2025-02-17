import requests
from static.js_py.Crud_filme import ChamaDB
class Pesquisa_nome_popular:
    def __init__(self,pesquisa):
        self.__pesquisa = pesquisa
        self.__SECRETKEY = '17528cca6d733031cd27a0916ee4cde5'


    def retorno(self):
        if self.__pesquisa:
            busca = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={self.__SECRETKEY}&language=pt-BR&query={self.__pesquisa}")
            busca = busca.json()
            busca = busca['results']
            for a in busca:
                return a['title']

class Pesquisa_Genero:
    def __init__(self,pesquisa):
        self.__pesquisa=pesquisa

    def retorno(self):
        resultados =[]          
        if self.__pesquisa:
            resultados = ChamaDB.filme.objects.filter(nome__icontains=self.__pesquisa)
            return resultados  
        