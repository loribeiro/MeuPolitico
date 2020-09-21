from . import connecting_api

rest_of_url1 = "/votacoes"
rest_of_url2 = "/votacoes/{id}"
rest_of_url3 = "/votacoes/{id}/orientacoes"
rest_of_url4 = "/votacoes/{id}/votos"

class Votacao:
    def __init__(self, **kwargs):
        self.id = kwargs["kwargs"]["id"]
        self.data = kwargs["kwargs"]["data"]
        self.aprovacao = kwargs["kwargs"]["aprovacao"]

class Voto:
    def __init__(self, **kwargs):
        self.deputado_id = kwargs["kwargs"]["deputado_"]["id"]
        self.tipo_voto = kwargs["kwargs"]["tipoVoto"]

def get_votacoes_proposicao(**kwargs):
    """
        Retorna uma lista de objetos do tipo Votacao.
        Parametros:
            kwargs: Dicionário contendo: 
                    - {dataInicio} e {dataFim} no formato AAAA-MM-DD
                    - {pagina} numero da pagina a ser retornado
                    - {idProposicao} a ser pesquisada as votacoes
    """
    votacoes = connecting_api.get_information(rest_of_url= rest_of_url1, kwargs= kwargs["kwargs"])
    lista_votacoes = []
    for votacao in votacoes["dados"]:
        lista_votacoes.append(Votacao(kwargs=votacao))
    
    return lista_votacoes

def get_voto_deputados(id_proposicao, **kwargs):
    """
        Retorna uma lista de objetos da classe Voto.
        Parametros:
            id_proposicao: Id da proposicao que se pretende extrair a votacao
        
    """
    votos = connecting_api.get_information(rest_of_url = rest_of_url4.format(id=id_proposicao))
    resultado_votos_lista = []
    for voto in votos["dados"]:
        resultado_votos_lista.append(Voto(kwargs=voto))
    
    return resultado_votos_lista
