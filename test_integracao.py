import pytest
import psycopg2
from unittest.mock import patch
import unittest
from modules.db import *
from modules import format_variables as format

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

    @patch('modules.db.cadastro_usuario')
    def test_botão_cadastro(self,mock_query):
        # Defina a resposta que você espera do banco de dados
        nome = 'Jaime Pascal Souto'
        email = 'exemplo.teste-123@email.com'
        dt_nascimento = '01/02/2004'
        telefone = '(71) 99402-2059'
        #cpf = '849.800.902-07'
        cpf = '858.816.885-51'
        senha = 'Ttrabalho321.'

        verifica_email = format.valida_email(email)
        cpf = format.format_cpf(cpf)
        telefone = format.format_telefone(telefone)
        data_nascimento = format.format_data(dt_nascimento)
        valida_senha = format.valida_senha(senha)

        if verifica_email == False or valida_senha == False or data_nascimento == False or telefone == False or cpf == False:
            raise ValueError('Algum campo informado está no formato inválido!!')

        else:

            resultado = verifica_cadastro(cpf)
            if not resultado.empty:
                # Exibir uma mensagem de erro se algum campo estiver fora do padrão necessário
                print('CPF ja cadastrado!')
                #raise ValueError('CPF ja cadastrado!')
            else:
                cadastro = cadastro_usuario(nome,email,senha,dt_nascimento,telefone,cpf)



                mock_query = pd.DataFrame([{'cpf': cpf, 'senha': senha}])
                mock_query.return_value = mock_query.to_string(index=False)
                
                
                resultado = pagina_login(cpf,senha)
                print(f'Resultado do usuario cadastrado:\n{resultado}')
                resultado = resultado[['cpf','senha']]
                resultado = resultado.to_string(index=False)

                assert resultado == mock_query.return_value

class TestBotaoAdicionar(unittest.TestCase):

    print('############### TESTES DE INTEGRAÇÃO - Botão de Adicionar ############################')

    @patch('modules.db.pagina_login')
    def test_botão_adicionar(self,mock_query):
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
    def test_botão_pesquisar(self,mock_query):
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
    def test_botão_atualizar(self,mock_query):
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
    def test_botão_deletar(self,mock_query):
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
    def test_botão_filtro_atendimentos(self,mock_query):
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
    def test_botão_filtro_receitas(self,mock_query):
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

    @patch('modules.db.atualiza_dados_cartao')
    def test_botão_cartao(self,mock_query):
        # Defina a resposta que você espera do banco de dados
        email = 'gabriela.santos@gmail.com'
        id_usuario = 7
        senha = 'Gabigol123.'
        telefone = '(71) 99702-2051'

        #verifica_email = format.valida_email(senha)
        telefone = format.format_telefone(telefone)
        valida_senha = format.valida_senha(senha)

        if  valida_senha == True and  telefone != False:  

            mock_query.return_value = True
            resultado = atualiza_dados_cartao(id_usuario,email,senha,telefone)
            assert resultado == mock_query.return_value
        else:
            raise ValueError('Algum campo informado está no formato inválido!!')

if __name__ == '__main__':
    unittest.main()

    
