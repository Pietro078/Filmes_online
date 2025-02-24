import re

class Tratamento_ep_name:
    def __init__(self, db):
        self.db = db
        
    def tra(self):
        lista = []
        nome = self.db
        for a in nome:
            clean_data = re.sub(r"[,()\[\]']", "", a.ep_name)  # Remove colchetes e aspas
            lista.append(clean_data)  # Adiciona a string completa à lista
        return lista