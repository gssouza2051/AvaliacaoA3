import pytest
import psycopg2
from modules import db

@pytest.fixture(scope='module')
def db_connection():
    # Conexão com o banco de dados de teste
    conn = psycopg2.connect(
        dbname='test_db',
        user='seu_usuario',
        password='sua_senha',
        host='localhost'
    )
    yield conn
    conn.close()

@pytest.fixture(scope='module')
def setup_database(db_connection):
    cursor = db_connection.cursor()
    # Criação de uma tabela de teste
    cursor.execute('''
        CREATE TABLE test_table (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100)
        )
    ''')
    db_connection.commit()
    yield
    # Limpeza após os testes
    cursor.execute('DROP TABLE test_table')
    db_connection.commit()
    cursor.close()

@pytest.fixture(scope='module')
def test_insert_data():
    cursor = db.connect()
    engine = db.conecta_db()
    #cursor.execute("INSERT INTO test_table (name) VALUES ('Teste')")
    #db_connection.commit()

    resultado_db = db.read("SELECT * FROM saude.tbl_usuarios", engine)
    #print(f'resultado :{resultado_db}')
    print(len(resultado_db))
    
    #assert len(resultado_db) == 10
    #assert rows[0][1] == 'Teste'

    cursor.close()

def test_example_1(test_insert_data):
    assert test_insert_data["key"] == "value"

if __name__ == '__main__':
    test_insert_data()
