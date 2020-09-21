from . import connecting_api
import pickle
import os

rest_of_url1 = "/referencias/proposicoes/codTema"
script_dir = os.path.dirname(__file__)
rel_path1 = "dados_serializados/dicionario_temas_votacoes.dat"
rel_path2 = "dados_serializados/lista_temas_votacoes.dat"

def update_codigos_temas():
    """
        Atualiza os arquivos com as informacoes dos temas das proposicoes.
        
        Esta funcao nao tem custo alto de execucao, no entanto nao deve ser
        executada se a lista de temas ja estiver registrada dado que o mesmo
        nao muda com frequencia
    """
    codigos = connecting_api.get_information(rest_of_url=rest_of_url1)
    dicionario_codigos = {}
    lista_temas = []
    for codigo in codigos["dados"]:
        dicionario_codigos[codigo["nome"]] = codigo["cod"]
        lista_temas.append(codigo["nome"])
    
    print(dicionario_codigos)
    abs_file_path1 = os.path.join(script_dir, rel_path1)
    abs_file_path2 = os.path.join(script_dir, rel_path2)
    file1 = open(abs_file_path1, 'wb')
    file2 = open(abs_file_path2, 'wb')
    pickle.dump(dicionario_codigos,file1,protocol=pickle.HIGHEST_PROTOCOL)
    pickle.dump(lista_temas,file2,protocol=pickle.HIGHEST_PROTOCOL)
    file1.close()
    file2.close()
    
def get_lista_temas():
    """
        Retorna uma lista com os nomes dos temas das proposicoes
    """
    abs_file_path1 = os.path.join(script_dir, rel_path2)
    temasFile = open(abs_file_path1,"rb")
    lista_temas = pickle.load(temasFile)
    temasFile.close()
    return lista_temas

def get_dict_temas():
    """
        Retorna um dicionario {tema : codigo}
    """
    abs_file_path2 = os.path.join(script_dir, rel_path1)
    dictFile =  open(abs_file_path2, 'rb')
    dict_temas = pickle.load(dictFile)
    dictFile.close()
    return dict_temas



