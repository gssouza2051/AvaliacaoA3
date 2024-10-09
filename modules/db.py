import pandas as pd
from sqlalchemy import create_engine
from modules import acessos
import psycopg2


def conecta_db():
    # Criando a string de conexão

    ferramenta = acessos.obter_credencial("database", "ferramenta")
    usuario = acessos.obter_credencial("database", "usuario")
    senha = acessos.obter_credencial("database", "senha")
    host = acessos.obter_credencial("database", "host")
    port = acessos.obter_credencial("database", "port")
    database = acessos.obter_credencial("database", "database")
    require = acessos.obter_credencial("database", "require")
    engine = create_engine(f"{ferramenta}://{usuario}:{senha}@{host}:{port}/{database}")
    return engine

def connect():
    ferramenta = acessos.obter_credencial("database", "ferramenta")
    usuario = acessos.obter_credencial("database", "usuario")
    senha = acessos.obter_credencial("database", "senha")
    host = acessos.obter_credencial("database", "host")
    port = acessos.obter_credencial("database", "port")
    database = acessos.obter_credencial("database", "database")
    require = acessos.obter_credencial("database", "require")

    conn = psycopg2.connect(
        host=host,
        database=database,
        user=usuario,
        password=senha,
        port=port,
        require=require
    )
    return conn



def read(consulta, engine):
    base = pd.read_sql_query(consulta, engine)
    return base


def write(df,table,schema, engine,payload=None):
    if payload:
        df = pd.DataFrame(data=payload, index=[0])
    df.to_sql(table, engine, schema=schema, if_exists='append', index=False)
    return True


def execute(conn, query):
    conn = connect()
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    cur.close()

#cadastro_usuarios()