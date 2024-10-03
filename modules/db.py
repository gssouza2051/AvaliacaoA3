import pandas as pd
from sqlalchemy import create_engine
from modules import acessos




def conecta_db():
    # Criando a string de conexão

    ferramenta = acessos.obter_credencial("database", "ferramenta")
    usuario = acessos.obter_credencial("database", "usuario")
    senha = acessos.obter_credencial("database", "senha")
    host = acessos.obter_credencial("database", "host")
    port = acessos.obter_credencial("database", "port")
    database = acessos.obter_credencial("database", "database")
    require = acessos.obter_credencial("database", "require")

    #engine = create_engine("postgresql://postgres:secreta007@localhost:5432/postgres")
    engine = create_engine(f"{ferramenta}://{usuario}:{senha}@{host}:{port}/{database}")
    return engine


def realiza_consulta_db(consulta, engine):
    base = pd.read_sql_query(consulta, engine)
    return base