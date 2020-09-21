from . import connecting_api
import pickle
import os

rest_of_url1 = "/proposicoes"
rest_of_url2 = "/proposicoes/{id}"
rest_of_url3 = "/proposicoes/{id}/autores"
rest_of_url4 = "/proposicoes/{id}/temas"
rest_of_url5 = "/proposicoes/{id}/votacoes"

class Proposicao:
    def __init__(self,**kwargs):
        self.id = kwargs["kwargs"]["id"]
        self.ano = kwargs["kwargs"]["ano"]
        self.ementa = kwargs["kwargs"]["ementa"]


def get_proposicoes(**kwargs):
    """
    Retorna uma lista com objetos do tipo Proposicao.

       Exemplo:
            kwargs={
                "codTema":"37",
                "itens":"100",
                "pagina":"4",
                "dataInicio":"2019-01-01",
                "dataFim":"2020-05-28"
                }
    """
    proposicoes = connecting_api.get_information(rest_of_url=rest_of_url1,kwargs= kwargs["kwargs"])
    lista_proposicoes = []
    for proposicao in proposicoes["dados"]:
        lista_proposicoes.append(Proposicao(kwargs=proposicao))
    
    return lista_proposicoes

#print(get_proposicoes(kwargs = {"codTema":"37","itens":"100","dataInicio":"2019-01-01","dataFim":"2020-05-28"}))