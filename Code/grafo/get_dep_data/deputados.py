from . import connecting_api
import pickle
import os

rest_of_url1 = "/deputados"
rest_of_url2 = "/deputados/{id}"
rest_of_url3 = "/deputados/{id}/despesas"
rest_of_url4 = "/deputados/{id}/frentes"
rest_of_url5 = "/deputados/{id}/orgaos"

class Deputado:
    def __init__(self,**kwargs):
        self.id = kwargs["kwargs"]["id"]
        self.nomeCivil = kwargs["kwargs"]["nomeCivil"]
        self.nome = kwargs["kwargs"]["ultimoStatus"]["nome"]
        self.nomeEleitoral =  kwargs["kwargs"]["ultimoStatus"]["nomeEleitoral"]
        self.siglaPartido =  kwargs["kwargs"]["ultimoStatus"]["siglaPartido"]
        self.siglaUf =  kwargs["kwargs"]["ultimoStatus"]["siglaUf"]
        self.dataNascimento = kwargs["kwargs"]['dataNascimento']
        self.ufNascimento = kwargs["kwargs"]["ufNascimento"]
        self.municipioNascimento = kwargs["kwargs"]["municipioNascimento"]

def update_deputados():
    """
        Esta função busca todos os deputados ativos, salva as informações de
        um por um na classe Deputado e salva um dicionario {id: Deputado}
        em um arquivo serializado.
        
        Atenção: Essa função é tem custo de tempo alto e deve ser evitada sempre
        que não ouver mudança nas informações. Para recuperar as informações use 
        get_deputados() ou para recuperar apenas a lista com os ids 
        get_lista_ids_deputados()  
    """
    deputados = connecting_api.get_information(rest_of_url=rest_of_url1)
    dicionario_deputados = { }
    lista_ids = []
    for deputado in deputados["dados"]:
        d = connecting_api.get_information(rest_of_url=rest_of_url2.format(id=deputado["id"]))
        lista_ids.append(deputado["id"])
        dicionario_deputados[deputado["id"]]=Deputado(kwargs=d["dados"])
    script_dir = os.path.dirname(__file__)
    rel_path1 = "dados_serializados/deputados.dat"
    rel_path2 = "dados_serializados/lista_ids.dat"
    abs_file_path1 = os.path.join(script_dir, rel_path1)
    abs_file_path2 = os.path.join(script_dir, rel_path2)
    file1 = open(abs_file_path1, 'wb')
    file2 = open(abs_file_path2, 'wb')
    pickle.dump(dicionario_deputados,file1,protocol=pickle.HIGHEST_PROTOCOL)
    pickle.dump(lista_ids,file2,protocol=pickle.HIGHEST_PROTOCOL)
    file1.close()
    file2.close()

def get_deputados():
    """
        Retorna um dicionario {id: Deputado}
         Importante: Se a função retornar um dicionario vazio execute update_deputados()
        e depois execute novamente get_deputados() 
    """
    script_dir = os.path.dirname(__file__)
    rel_path1 = "dados_serializados/deputados.dat"
    abs_file_path1 = os.path.join(script_dir, rel_path1)
    deputadoFile = open(abs_file_path1,"rb") 
    dicionario_deputados = pickle.load(deputadoFile)
    deputadoFile.close()
    return dicionario_deputados

def get_lista_ids_deputados():
    """
        Retorna uma lista com todos os ids dos deputados ativos
    """
    script_dir = os.path.dirname(__file__)
    rel_path2 = "dados_serializados/lista_ids.dat"
    abs_file_path1 = os.path.join(script_dir, rel_path2)
    idsFile = open(abs_file_path1,"rb")
    lista_ids = pickle.load(idsFile)
    idsFile.close()
    return lista_ids

def get_despesas_deputados(id, **kwargs):
    """
        Esta função retorna um dicionário com os gastos do deputado pesquisado.
        Esta função pode receber como parametro um dicionario contendo:
            ano: ano em que se deseja checar as despesas
            itens: quantidade maxima de itens por pagina (maximo = 100 e padrao = 15)
            pagina: Importante! Se a pagina for omitida será retornada apenas a primeira
                -(Dica) chame essa função em loop while aumentando o valor da pagina em 1 
                até o len(get_despesas_deputados) retornar 0 
    """
    
    if kwargs == {}:
        resposta = connecting_api.get_information(rest_of_url3.format(id = id))
    else:
        resposta = connecting_api.get_information(rest_of_url3.format(id = id), kwargs= kwargs["kwargs"])
    
    return resposta["dados"]

#TODO: Implentar função para recuperar as frentes
def get_frentes_politicas(id):
    resposta = connecting_api.get_information(rest_of_url=rest_of_url4.format(id=id))
    return resposta

#TODO: Implementar função para recuperar orgãos 
def get_orgaos(id):
    resposta = connecting_api.get_information(rest_of_url=rest_of_url5.format(id=id))
    return resposta

#print(len(get_despesas_deputados(id=74156, kwargs={"ano":"2019", "itens":"100","pagina":"5"})))
#print(get_deputados())