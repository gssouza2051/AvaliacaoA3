import pytest
import psycopg2
from unittest.mock import patch
import unittest
from modules.db import *

'''
Em Python, a biblioteca unittest.mock é excelente para criar objetos de mock, simulando comportamentos de funções e métodos que interagem com o banco de dados.
A função mock.patch() permite substituir dependências externas (como chamadas de banco de dados) por versões de mock dentro de um contexto específico.
'''

class TestBotaoLogin(unittest.TestCase):

    print('############### TESTES DE INTEGRAÇÃO - Botão de Login ############################')

    @patch('modules.db.pagina_login')
    def test_botão_login(self,mock_query):
        # Defina a resposta que você espera do banco de dados
        cpf = '858.816.885-51'
        senha = 'Gabigol123.'
        mock_query = pd.DataFrame([{'cpf': cpf, 'senha': senha}])
        mock_query.return_value = mock_query.to_string(index=False)
        
        resultado = pagina_login(cpf,senha)
        resultado = resultado[['cpf','senha']]
        resultado = resultado.to_string(index=False)

        assert resultado == mock_query.return_value

class TestBotaoCadastro(unittest.TestCase):

    print('############### TESTES DE INTEGRAÇÃO - Botão de cadastro ############################')

    @patch('modules.db.pagina_login')
    def test_botão_login(self,mock_query):
        # Defina a resposta que você espera do banco de dados
        cpf = '858.816.885-51'
        senha = 'Gabigol123.'
        mock_query = pd.DataFrame([{'cpf': cpf, 'senha': senha}])
        mock_query.return_value = mock_query.to_string(index=False)
        
        resultado = pagina_login(cpf,senha)
        resultado = resultado[['cpf','senha']]
        resultado = resultado.to_string(index=False)

        assert resultado == mock_query.return_value

class TestBotaoAdicionar(unittest.TestCase):

    print('############### TESTES DE INTEGRAÇÃO - Botão de Adicionar ############################')

    @patch('modules.db.pagina_login')
    def test_botão_login(self,mock_query):
        # Defina a resposta que você espera do banco de dados
        cpf = '858.816.885-51'
        senha = 'Gabigol123.'
        mock_query = pd.DataFrame([{'cpf': cpf, 'senha': senha}])
        mock_query.return_value = mock_query.to_string(index=False)
        
        resultado = pagina_login(cpf,senha)
        resultado = resultado[['cpf','senha']]
        resultado = resultado.to_string(index=False)

        assert resultado == mock_query.return_value

class TestBotaoPesquisar(unittest.TestCase):

    print('############### TESTES DE INTEGRAÇÃO - Botão de Pesquisar ############################')

    @patch('modules.db.pagina_login')
    def test_botão_login(self,mock_query):
        # Defina a resposta que você espera do banco de dados
        cpf = '858.816.885-51'
        senha = 'Gabigol123.'
        mock_query = pd.DataFrame([{'cpf': cpf, 'senha': senha}])
        mock_query.return_value = mock_query.to_string(index=False)
        
        resultado = pagina_login(cpf,senha)
        resultado = resultado[['cpf','senha']]
        resultado = resultado.to_string(index=False)

        assert resultado == mock_query.return_value

class TestBotaoAtualizar(unittest.TestCase):

    print('############### TESTES DE INTEGRAÇÃO - Botão de Atualizar ############################')

    @patch('modules.db.pagina_login')
    def test_botão_login(self,mock_query):
        # Defina a resposta que você espera do banco de dados
        cpf = '858.816.885-51'
        senha = 'Gabigol123.'
        mock_query = pd.DataFrame([{'cpf': cpf, 'senha': senha}])
        mock_query.return_value = mock_query.to_string(index=False)
        
        resultado = pagina_login(cpf,senha)
        resultado = resultado[['cpf','senha']]
        resultado = resultado.to_string(index=False)

        assert resultado == mock_query.return_value

class TestBotaoDeletar(unittest.TestCase):

    print('############### TESTES DE INTEGRAÇÃO - Botão de Deletar ############################')

    @patch('modules.db.pagina_login')
    def test_botão_login(self,mock_query):
        # Defina a resposta que você espera do banco de dados
        cpf = '858.816.885-51'
        senha = 'Gabigol123.'
        mock_query = pd.DataFrame([{'cpf': cpf, 'senha': senha}])
        mock_query.return_value = mock_query.to_string(index=False)
        
        resultado = pagina_login(cpf,senha)
        resultado = resultado[['cpf','senha']]
        resultado = resultado.to_string(index=False)

        assert resultado == mock_query.return_value

class TestBotaoLimpar(unittest.TestCase):

    print('############### TESTES DE INTEGRAÇÃO - Botão de Limpar ############################')

    @patch('modules.db.pagina_login')
    def test_botão_login(self,mock_query):
        # Defina a resposta que você espera do banco de dados
        cpf = '858.816.885-51'
        senha = 'Gabigol123.'
        mock_query = pd.DataFrame([{'cpf': cpf, 'senha': senha}])
        mock_query.return_value = mock_query.to_string(index=False)
        
        resultado = pagina_login(cpf,senha)
        resultado = resultado[['cpf','senha']]
        resultado = resultado.to_string(index=False)

        assert resultado == mock_query.return_value

class TestBotaoFiltroHistoricoAtendimentos(unittest.TestCase):

    print('############### TESTES DE INTEGRAÇÃO - Botão de filtrar Histórico de Atendimentos ############################')

    @patch('modules.db.pagina_login')
    def test_botão_login(self,mock_query):
        # Defina a resposta que você espera do banco de dados
        cpf = '858.816.885-51'
        senha = 'Gabigol123.'
        mock_query = pd.DataFrame([{'cpf': cpf, 'senha': senha}])
        mock_query.return_value = mock_query.to_string(index=False)
        
        resultado = pagina_login(cpf,senha)
        resultado = resultado[['cpf','senha']]
        resultado = resultado.to_string(index=False)

        assert resultado == mock_query.return_value

class TestBotaoFiltroHistoricoReceitas(unittest.TestCase):

    print('############### TESTES DE INTEGRAÇÃO - Botão de filtrar Histórico de Receitas ############################')

    @patch('modules.db.pagina_login')
    def test_botão_login(self,mock_query):
        # Defina a resposta que você espera do banco de dados
        cpf = '858.816.885-51'
        senha = 'Gabigol123.'
        mock_query = pd.DataFrame([{'cpf': cpf, 'senha': senha}])
        mock_query.return_value = mock_query.to_string(index=False)
        
        resultado = pagina_login(cpf,senha)
        resultado = resultado[['cpf','senha']]
        resultado = resultado.to_string(index=False)

        assert resultado == mock_query.return_value

class TestBotaoAtualizarCartao(unittest.TestCase):

    print('############### TESTES DE INTEGRAÇÃO - Botão de Atualizar cartão ############################')

    @patch('modules.db.pagina_login')
    def test_botão_login(self,mock_query):
        # Defina a resposta que você espera do banco de dados
        cpf = '858.816.885-51'
        senha = 'Gabigol123.'
        mock_query = pd.DataFrame([{'cpf': cpf, 'senha': senha}])
        mock_query.return_value = mock_query.to_string(index=False)
        
        resultado = pagina_login(cpf,senha)
        resultado = resultado[['cpf','senha']]
        resultado = resultado.to_string(index=False)

        assert resultado == mock_query.return_value

class TestBotaoPermissao(unittest.TestCase):

    print('############### TESTES DE INTEGRAÇÃO - Permissões  ############################')

    @patch('modules.db.pagina_login')
    def test_botão_login(self,mock_query):
        # Defina a resposta que você espera do banco de dados
        cpf = '858.816.885-51'
        senha = 'Gabigol123.'
        mock_query = pd.DataFrame([{'cpf': cpf, 'senha': senha}])
        mock_query.return_value = mock_query.to_string(index=False)
        
        resultado = pagina_login(cpf,senha)
        resultado = resultado[['cpf','senha']]
        resultado = resultado.to_string(index=False)

        assert resultado == mock_query.return_value


if __name__ == '__main__':
    unittest.main()

    
