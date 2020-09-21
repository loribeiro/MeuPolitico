import get_dep_data.get_data_interface as informacoes
from get_dep_data.deputados import Deputado
import tratamento_dados.grafo as g
import db.db_interface as db
from multiprocessing import Process
import matplotlib.pyplot as plt
import networkx as nx
import sys
import pickle
import os



script_dir = os.path.dirname(__file__)
rel_path1 = "grafos_gerados"
abs_file_path = os.path.join(script_dir, rel_path1)

def criar_grafo(tema):
    meu_grafo = g.Graph(informacoes.lista_ids_deputados())
    print(meu_grafo.get_edges())
    proposicoes = db.retrieve_proposicoes_tema(tema)
    a = []
    for proposicao in proposicoes:
        a.append(proposicao["id"])
        #print(proposicao["id"])


    #print(a)
    for codigo in a:
        votacoes = db.retrieve_votacoes_por_codigo(codigo)
        #print(votacoes[0]["codigo"])
        for votacao in votacoes:
            voto = db.retrieve_voto_deputados_proposicao(votacao["codigo"])
            voto_sim = [v["deputado_id"] for v in voto if v["tipo_voto"] == "Sim"]
            voto_nao = [v["deputado_id"] for v in voto if v["tipo_voto"] == "Não"]
            voto_obstrucao = [v["deputado_id"] for v in voto if v["tipo_voto"] == "Obstrução"]
            voto_abstencao = [v["deputado_id"] for v in voto if v["tipo_voto"] == "Abstenção"]
            voto_17 = [v["deputado_id"] for v in voto if v["tipo_voto"] == "Artigo 17"]
            print("votos sim: ",len(voto_sim))
            print("votos nao: ",len(voto_nao))
            meu_grafo.add_edges_from_list(voto_sim)
            meu_grafo.add_edges_from_list(voto_nao)
            meu_grafo.add_edges_from_list(voto_obstrucao)
            meu_grafo.add_edges_from_list(voto_abstencao)
            meu_grafo.add_edges_from_list(voto_17)

    print(meu_grafo.get_edges())
    file_name = str(tema)+".dat"
    abs_file_path1 = os.path.join(abs_file_path, file_name )
    file1 = open(abs_file_path1, 'wb')
    pickle.dump(meu_grafo,file1,protocol=pickle.HIGHEST_PROTOCOL)
    file1.close()   

def converter_para_gephi(tema):
    nome_arquivo = str(tema)+".dat"
    abs_file_path1 = os.path.join(abs_file_path, nome_arquivo)
    file1 = open(abs_file_path1, 'rb')
    grafo = pickle.load(file1)
    file1.close()
    edges = grafo.get_edges()
    G = nx.Graph()
    ids = informacoes.lista_ids_deputados()
    for edge in edges:
        if ids.count(edge[0]) > 0 and ids.count(edge[1])>0:  
            G.add_edge(edge[0], edge[1], weight=edges[edge])
        else:
            print("pegou um deputado intruso!")
    
    nome_arquivo_gephi = str(tema)+".gexf"
    nx.write_gexf(G, nome_arquivo_gephi) 

temas = informacoes.lista_temas_proposicoes()
dic_temas = informacoes.dict_temas_proposicoes()
for tema in temas:
    if dic_temas[tema] !="48":
        converter_para_gephi(dic_temas[tema])