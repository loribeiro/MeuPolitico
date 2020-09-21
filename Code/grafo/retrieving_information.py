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


def recuperando_e_salvando_votos(id_votacao):
    votos =informacoes.voto_deputados_proposicao(id_votacao)
    for voto in votos:
        db.save_voto_deputados_proposicao(id_votacao,voto.deputado_id, voto.tipo_voto)
        print("salvo, codigo:",id_votacao)

def recuperando_e_salvando_proposicoes(nome_tema, tema_id):
    print("tema: ", nome_tema)
    props = informacoes.proposicoes_do_tema(tema=nome_tema,data_inicio="2019-01-01",data_fim="2019-12-28")
    for prop in props:
        db.save_proposicoes_tema(prop.id,prop.ano,prop.ementa,tema_id)
        print("Proposicao: ", prop.id)    

def recuperando_e_salvando_votacoes(prop_id):
    votacoes = informacoes.votacoes_por_proposicao(prop_id, "2019-01-01","2019-02-28")
    for votacao in votacoes:
        db.save_votacoes_proposicao(votacao.id, votacao.data, votacao.aprovacao,prop_id)
        print("Salvo votacao: ", votacao.id)

def chunkify(lst,n):
    return [lst[i::n] for i in range(n)]

def manager(votacoes):
    for votacao in votacoes:
        print("Id da votacao",votacao["codigo"])    
        recuperando_e_salvando_votos(votacao["codigo"])

vot = db.retrieve_votacoes_proposicao()
nova_lista = chunkify(vot, 3)
print("votacoes ", len(nova_lista[0]))
manager(nova_lista[0])
p1 = Process(target=manager, args = [nova_lista[0]])
p2 = Process(target=manager, args = [nova_lista[1]])
p3 = Process(target=manager, args = [nova_lista[2]])
p1.start()
p2.start()
p3.start()
