from .deputados import Deputado, get_deputados, get_lista_ids_deputados, get_despesas_deputados, get_frentes_politicas, get_orgaos
from .referencias import get_lista_temas, get_dict_temas
from .votacoes import Votacao, Voto, get_votacoes_proposicao, get_voto_deputados
from .proposicoes import Proposicao, get_proposicoes

def lista_temas_proposicoes():
    return get_lista_temas()

def dict_temas_proposicoes():
    return get_dict_temas()

def proposicoes_do_tema(tema, data_inicio, data_fim):
    """
        Retorna uma lista de objetos do tipo Proposicao
         Parametros:
            -tema: nome do tema escolhido (consulte a lista com a funcao lista_temas_proposicoes())
            -data_inicio e data_fim: formato yyyy-mm-dd
    """
    id_tema = get_dict_temas()[tema]
    cont = 1
    lista_proposicoes = []
    while True:
        resultado = get_proposicoes(kwargs={"codTema": id_tema,"itens":"100","pagina":cont,"dataInicio":data_inicio,"dataFim":data_fim})
        print("Iteracao: ",cont)
        print("len: ",len(resultado))
        if len(resultado) == 0:
            break
        lista_proposicoes = lista_proposicoes + resultado
        cont = cont+1
    
    return lista_proposicoes

def votacoes_por_proposicao(id_proposicao,  data_inicio, data_fim):
    cont=1
    lista_votacoes = []
    while True:
        print("andando ",cont)
        resultado = get_votacoes_proposicao(kwargs={"dataInicio":data_inicio, "dataFim":data_fim, "idProposicao":id_proposicao,"pagina":cont})
        if len(resultado) == 0:
            break
        lista_votacoes = lista_votacoes + resultado
        cont = cont+1
    print("retornando")
    return lista_votacoes

def voto_deputados_proposicao(id_proposicao):
    """
        Retorna uma lista de objetos do tipo Voto
    """
    return get_voto_deputados(id_proposicao=id_proposicao)

def lista_ids_deputados():
    return get_lista_ids_deputados()

def dicionario_deputados():
    return get_deputados()

def despesas_deputado(id_deputado, ano):
    cont = 1
    lista_despesas = []
    while True:
        print("requisitando", cont)
        resultado = get_despesas_deputados(id_deputado,kwargs={"ano":ano,"pagina":cont, "itens":100})

#lista_resposta = []
#a = proposicoes_do_tema("Defesa e Segurança", "2019-01-01","2019-12-31")
#for ele in a:
#    lista_resposta.append(ele.ementa)
#print(lista_resposta)