import sqlite3
import os

path = os.path.dirname(os.path.abspath(__file__))
arquivo = os.path.join(path, 'db.sqlite')
conn = sqlite3.connect(arquivo)
conn.row_factory = sqlite3.Row
cur = conn.cursor()
cur.executescript('''

CREATE TABLE IF NOT EXISTS Deputado (
    id  INTEGER NOT NULL PRIMARY KEY  UNIQUE,
    nome_civil    TEXT,
    nome TEXT,
    nomeEleitoral TEXT,
    siglaPartido TEXT,
    siglaUf TEXT,
    dataNascimento TEXT,
    ufNascimento TEXT,
    municipioNascimento TEXT
);

CREATE TABLE IF NOT EXISTS Voto (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    deputado_id INTEGER NOT NULL,
    tipo_voto TEXT,
    votacao_id INTEGER NOT NULL
);


CREATE TABLE IF NOT EXISTS Votacao (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    codigo TEXT UNIQUE,
    data  TEXT,
    aprovacao   TEXT
    proposicao_id INTEGER
);

CREATE TABLE IF NOT EXISTS Proposicao (
    id  INTEGER NOT NULL PRIMARY KEY,
    ano  TEXT,
    ementa   TEXT,
    tema_id  INTEGER
);

CREATE TABLE IF NOT EXISTS Temas (
    codigo  INTEGER NOT NULL PRIMARY KEY UNIQUE,
    nome TEXT  UNIQUE
    
);
''')

def save_deputado(deputado):
    cur.execute('''INSERT INTO Deputado
        (id, nome_civil, nome, nomeEleitoral, siglaPartido,siglaUf,
         dataNascimento,ufNascimento, municipioNascimento) 
        VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
        ( deputado.id, deputado.nomeCivil,deputado.nome, deputado.nomeEleitoral, deputado.siglaPartido, 
        deputado.siglaUf, deputado.dataNascimento, deputado.ufNascimento, deputado.municipioNascimento) )
    
    conn.commit()


def retrieve_deputado():
    cur.execute('SELECT * FROM Deputado')
    deputados = cur.fetchall()
    conn.commit()

    return deputados



def save_temas_proposicoes(codigo,nome):
    cur.execute('''INSERT INTO Temas
    (codigo,nome)
    VALUES(?,?)''',(codigo,nome))

    conn.commit()

def retrieve_temas_proposicoes():
    cur.execute('SELECT * FROM Temas')
    temas = cur.fetchall()
    conn.commit()

    return temas

def save_proposicoes_tema(id,ano,ementa,tema_id):
    cur.execute('''INSERT  OR IGNORE INTO Proposicao
    (id,ano,ementa,tema_id)
    VALUES(?,?,?,?)''',(id,ano,ementa,tema_id))
    conn.commit()

def retrieve_proposicoes_tema(tema_id):
    cur.execute('''SELECT * FROM Proposicao 
    where Proposicao.tema_id = ?''',[tema_id])
    proposicoes = cur.fetchall()
    conn.commit()

    return proposicoes

def retrieve_todas_proposicoes_tema():
    cur.execute("""select distinct(Proposicao.id)
                        from Proposicao
                        where Proposicao.id not in (
                            select distinct(Votacao.proposicao_id)
                            from Votacao
                )""")
    proposicoes = cur.fetchall()
    conn.commit()

    return proposicoes

def save_votacoes_proposicao(codigo, data, aprovacao,proposicao_id):
    try:
        cur.execute('''INSERT OR IGNORE INTO Votacao
        (codigo,data,aprovacao,proposicao_id)
        VALUES(?,?,?,?)''',(codigo,data,aprovacao,proposicao_id))
        conn.commit()
    except sqlite3.OperationalError:
        print ("falhou")

def retrieve_votacoes_proposicao():
    cur.execute("""
        select distinct(Votacao.codigo)
        from Votacao
        where Votacao.aprovacao <> "NULL"
    """)
    votacoes= cur.fetchall()
    conn.commit()

    return votacoes

def retrieve_votacoes_por_codigo(proposicao_id):
    cur.execute('''
        select Votacao.codigo
        from Votacao
        where Votacao.proposicao_id = ?
    ''',[proposicao_id])
    votacoes = cur.fetchall()
    conn.commit()

    return votacoes

def save_voto_deputados_proposicao(id_votacao,deputado_id,tipo_voto):
    cur.execute('''INSERT OR IGNORE INTO Voto
        (deputado_id,tipo_voto,votacao_id)
        VALUES(?,?,?)''',(deputado_id,tipo_voto,id_votacao))
    conn.commit()

def retrieve_voto_deputados_proposicao(votacao_id):
    cur.execute('''SELECT * FROM Voto 
    where Voto.votacao_id = ?''',[votacao_id])
    votos = cur.fetchall()
    conn.commit()

    return votos



