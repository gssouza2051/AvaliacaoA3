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

class TestBotaoAdicionarAtendimentos(unittest.TestCase):

    print('############### TESTES DE INTEGRAÇÃO - Botão de Adicionar na tela de Atendimentos ############################')

    @patch('modules.db.adicionar_atendimentos')
    def test_botão_adicionar_atendimentos_ja_existente(self,mock_query):
        # Defina a resposta que você espera do banco de dados
        tree = None
        nome = 'Gabriel Araujo Rocha'
        medico = 'Matheus Garcia Lopes'
        data_consulta = '07/10/2024'
        horario_consulta = '11:00:00'
        especialidade = 'Pediatria'
        cpf = '858.816.885-51'

        mock_query.return_value = 'Médico ja possui outro atendimento nessa data e horário!!'
        
        resultado = adicionar_atendimentos(tree, nome, medico, data_consulta, horario_consulta, especialidade, cpf)

        assert resultado == mock_query.return_value

    @patch('modules.db.adicionar_atendimentos')
    def test_botão_adicionar_atendimentos_campos_vazios(self,mock_query):
        # Defina a resposta que você espera do banco de dados
        tree = None
        nome = ''
        medico = ''
        data_consulta = ''
        horario_consulta = ''
        especialidade = ''
        cpf = '858.816.885-51'

        mock_query.return_value = 'Preencha pelo menos os campos : Data da consulta, Horário, médico, paciente  e especialidade por favor!'
        
        resultado = adicionar_atendimentos(tree, nome, medico, data_consulta, horario_consulta, especialidade, cpf)

        assert resultado == mock_query.return_value

    @patch('modules.db.adicionar_atendimentos')
    def test_botão_adicionar_atendimentos_paciente_inexistente(self,mock_query):
        # Defina a resposta que você espera do banco de dados
        tree = None
        nome = 'TESTE'
        medico = 'Matheus Garcia Lopes'
        data_consulta = '07/10/2024'
        horario_consulta = '11:00:00'
        especialidade = 'Pediatria'
        cpf = '858.816.885-51'

        mock_query.return_value = 'O Paciente não possui cadastro na plataforma para ter um atendimento cadastrado'
        
        resultado = adicionar_atendimentos(tree, nome, medico, data_consulta, horario_consulta, especialidade, cpf)

        assert resultado == mock_query.return_value

    @patch('modules.db.adicionar_atendimentos')
    def test_botão_adicionar_atendimentos_permissao_negada(self,mock_query):
        # Defina a resposta que você espera do banco de dados
        tree = None
        nome = 'Fernanda Lima Martins'
        medico = 'Matheus Garcia Lopes'
        data_consulta = '07/10/2024'
        horario_consulta = '11:00:00'
        especialidade = 'Pediatria'
        cpf = '678.901.234-55'

        mock_query.return_value = 'Você não pode adicionar nenhum atendimento'
        
        resultado = adicionar_atendimentos(tree, nome, medico, data_consulta, horario_consulta, especialidade, cpf)

        assert resultado == mock_query.return_value

    @patch('modules.db.adicionar_atendimentos')
    def test_botão_adicionar_atendimentos_data_errada(self,mock_query):
        # Defina a resposta que você espera do banco de dados
        tree = None
        nome = 'Gabriel Araujo Rocha'
        medico = 'Matheus Garcia Lopes'
        data_consulta = '2024-01-01'
        horario_consulta = '11:00:00'
        especialidade = 'Pediatria'
        cpf = '858.816.885-51'

        mock_query.return_value = 'Insira a data no formato correto (DD/MM/YYYY)!'
        
        resultado = adicionar_atendimentos(tree, nome, medico, data_consulta, horario_consulta, especialidade, cpf)

        assert resultado == mock_query.return_value

class TestBotaoPesquisarAtendimentos(unittest.TestCase):

    print('############### TESTES DE INTEGRAÇÃO - Botão de Pesquisar na tela de Atendimentos ############################')

    @patch('modules.db.pesquisar_atendimentos')
    def test_botão_pesquisar_atendimentos_correto(self,mock_query):
        # Defina a resposta que você espera do banco de dados
        tree = None
        nome = 'Camila Ferreira Lima'
        medico = 'Graciele Almeida Nunes'
        data_consulta = '03/10/2024'
        horario_consulta = '08:00:00'
        plano_saude = 'Amil'
        status = 'Pendente'
        especialidade = 'Fisioterapeuta'
        cpf = '858.816.885-51'

        mock_query.return_value = [['Camila Ferreira Lima', 'Graciele Almeida Nunes', 'Amil', '03/10/2024', datetime.time(8, 0), 'Fisioterapeuta', 'Pendente']]

        resultado = pesquisar_atendimentos(tree, nome, medico, data_consulta, horario_consulta, plano_saude, status, especialidade, cpf)

        assert resultado == mock_query.return_value

    @patch('modules.db.pesquisar_atendimentos')
    def test_botão_pesquisar_atendimentos_campos_vazios(self,mock_query):
        # Defina a resposta que você espera do banco de dados
        tree = None
        nome = ''
        medico = ''
        data_consulta = ''
        horario_consulta = ''
        plano_saude = ''
        status = ''
        especialidade = ''
        cpf = '858.816.885-51'

        mock_query.return_value = 'Preencha pelo menos os campos : Data da consulta, Especialidade, Horário, Status e médico por favor!'

        resultado = pesquisar_atendimentos(tree, nome, medico, data_consulta, horario_consulta, plano_saude, status, especialidade, cpf)

        assert resultado == mock_query.return_value

    @patch('modules.db.pesquisar_atendimentos')
    def test_botão_pesquisar_atendimentos_data_invalida(self,mock_query):
        # Defina a resposta que você espera do banco de dados
        tree = None
        nome = 'Camila Ferreira Lima'
        medico = 'Graciele Almeida Nunes'
        data_consulta = '2024-01-02'
        horario_consulta = '08:00:00'
        plano_saude = 'Amil'
        status = 'Pendente'
        especialidade = 'Fisioterapeuta'
        cpf = '858.816.885-51'

        mock_query.return_value = 'Insira a data no formato correto (DD/MM/YYYY)!'

        resultado = pesquisar_atendimentos(tree, nome, medico, data_consulta, horario_consulta, plano_saude, status, especialidade, cpf)

        assert resultado == mock_query.return_value

    @patch('modules.db.pesquisar_atendimentos')
    def test_botão_pesquisar_atendimentos_nao_encontrado(self,mock_query):
        # Defina a resposta que você espera do banco de dados
        tree = None
        nome = 'teste'
        medico = 'teste'
        data_consulta = '07/02/2024'
        horario_consulta = '11:00:00'
        plano_saude = 'Amil'
        status = 'Pendente'
        especialidade = 'Ginecologista'
        cpf = '858.816.885-51'

        mock_query.return_value = 'Procuramos pelos seus filtros e não foi encontrado nenhum atendimento!'

        resultado = pesquisar_atendimentos(tree, nome, medico, data_consulta, horario_consulta, plano_saude, status, especialidade, cpf)

        assert resultado == mock_query.return_value

class TestBotaoAtualizarAtendimentos(unittest.TestCase):

    print('############### TESTES DE INTEGRAÇÃO - Botão de Atualizar na tela de Atendimentos ############################')

    @patch('modules.db.update_atendimentos')
    def test_botão_atualizar_atendimentos(self,mock_query):
        # Defina a resposta que você espera do banco de dados

        #Obs: Não foi possível realizar o teste nessa classe
        tree = None
        nome = 'Camila Ferreira Lima'
        medico = 'Graciele Almeida Nunes'
        data_consulta = '10/03/2024'
        horario_consulta = '08:00:00'
        status = 'Pendente'
        cpf = '858.816.885-51'

        '''mock_query = pd.DataFrame([{'cpf': cpf, 'senha': senha}])
        mock_query.return_value = mock_query.to_string(index=False)
        
        resultado = update_atendimentos(tree, cpf, nome, medico, status, data_consulta, horario_consulta)
        resultado = resultado[['cpf','senha']]
        resultado = resultado.to_string(index=False)

        assert resultado == mock_query.return_value'''

class TestBotaoDeletarAtendimentos(unittest.TestCase):

    print('############### TESTES DE INTEGRAÇÃO - Botão de Deletar na tela de Atendimentos ############################')

    @patch('modules.db.deletar_atendimentos')
    def test_botão_deletar_atendimentos(self,mock_query):
        # Defina a resposta que você espera do banco de dados
        #Obs: Não foi possível realizar o teste nessa classe
        tree = None
        medico = 'Matheus Garcia Lopes'
        data_consulta = '01/01/2024'
        horario_consulta = '09:00:00'
        status = 'Pendente'
        cpf = '858.816.885-51'

        '''mock_query = pd.DataFrame([{'cpf': cpf, 'senha': senha}])
        mock_query.return_value = mock_query.to_string(index=False)
        
        resultado = deletar_atendimentos(tree, cpf, medico, data_consulta, horario_consulta, status)
        resultado = resultado[['cpf','senha']]
        resultado = resultado.to_string(index=False)

        assert resultado == mock_query.return_value'''


class TestBotaoAdicionarReceita(unittest.TestCase):

    print('############### TESTES DE INTEGRAÇÃO - Botão de Adicionar na tela de Receita ############################')

    @patch('modules.db.adicionar_receita')
    def test_botão_adicionar_receita_ja_existente(self,mock_query):
        # Defina a resposta que você espera do banco de dados
        
        tree = None
        nome = 'Jurandir Rosa Martins'
        medico = 'Matheus Garcia Lopes'
        medicamento = 'Dorflex'
        atestado = 'Atestado de 2 dias'
        descricao = 'Para dor leve a moderada'
        data_consulta = '01/01/2024'
        horario_consulta = '09:00:00'
        cpf = '858.816.885-51'

        mock_query.return_value = 'Receita ja existe!!'
        
        resultado = adicionar_receita(tree, nome, medico, medicamento, atestado, descricao, data_consulta, horario_consulta, cpf)

        assert resultado == mock_query.return_value
    
    @patch('modules.db.adicionar_receita')
    def test_botão_adicionar_receita_campos_vazios(self,mock_query):
        # Defina a resposta que você espera do banco de dados
        
        tree = None
        nome = ''
        medico = ''
        medicamento = ''
        atestado = ''
        descricao = ''
        data_consulta = ''
        horario_consulta = ''
        cpf = '858.816.885-51'

        mock_query.return_value = 'Preencha todos os campos por favor'
        
        resultado = adicionar_receita(tree, nome, medico, medicamento, atestado, descricao, data_consulta, horario_consulta, cpf)

        assert resultado == mock_query.return_value

    
    @patch('modules.db.adicionar_receita')
    def test_botão_adicionar_receita_data_invalida(self,mock_query):
        # Defina a resposta que você espera do banco de dados
        
        tree = None
        nome = 'Jurandir Rosa Martins'
        medico = 'Matheus Garcia Lopes'
        medicamento = 'Dorflex'
        atestado = 'Atestado de 2 dias'
        descricao = 'Para dor leve a moderada'
        data_consulta = '2024-01-01'
        horario_consulta = '09:00:00'
        cpf = '858.816.885-51'

        mock_query.return_value = 'Insira a data no formato correto (DD/MM/YYYY)!'
        
        resultado = adicionar_receita(tree, nome, medico, medicamento, atestado, descricao, data_consulta, horario_consulta, cpf)

        assert resultado == mock_query.return_value


    @patch('modules.db.adicionar_receita')
    def test_botão_adicionar_receita_paciente_inexistente(self,mock_query):
        # Defina a resposta que você espera do banco de dados
        
        tree = None
        nome = 'TESTE'
        medico = 'Matheus Garcia Lopes'
        medicamento = 'Dorflex'
        atestado = 'Atestado de 2 dias'
        descricao = 'Para dor leve a moderada'
        data_consulta = '10/08/2024'
        horario_consulta = '11:00:00'
        cpf = '858.816.885-51'

        mock_query.return_value = 'Não existe esse paciente cadastrado no nosso sistema!!'
        
        resultado = adicionar_receita(tree, nome, medico, medicamento, atestado, descricao, data_consulta, horario_consulta, cpf)

        assert resultado == mock_query.return_value


    @patch('modules.db.adicionar_receita')
    def test_botão_adicionar_receita_permissao(self,mock_query):
        # Defina a resposta que você espera do banco de dados
        
        tree = None
        nome = 'Jurandir Rosa Martins'
        medico = 'Matheus Garcia Lopes'
        medicamento = 'Dorflex'
        atestado = 'Atestado de 2 dias'
        descricao = 'Para dor leve a moderada'
        data_consulta = '01/01/2024'
        horario_consulta = '09:00:00'
        cpf = '678.901.234-55'

        mock_query.return_value = 'Você não pode adicionar nenhuma receita'
        
        resultado = adicionar_receita(tree, nome, medico, medicamento, atestado, descricao, data_consulta, horario_consulta, cpf)

        assert resultado == mock_query.return_value



class TestBotaoPesquisarReceita(unittest.TestCase):

    print('############### TESTES DE INTEGRAÇÃO - Botão de Pesquisar na tela de Receita ############################')

    @patch('modules.db.pesquisar_receita')
    def test_botão_pesquisar_receita_correta(self,mock_query):
        # Defina a resposta que você espera do banco de dados
        tree = None
        medico = 'Ana Clara Souza'
        data_consulta = '15/10/2024'
        horario_consulta = '15:00:00'
        cpf = '858.816.885-51'

        mock_query.return_value = [['Otavio Ribeiro Nunes', 'Ana Clara Souza', '15/10/2024', datetime.time(15, 0), 'Corticoide para inflamações e doenças autoimunes', 'Prednisona', 'Atestado de 1 dia']]
        
        resultado = pesquisar_receita(tree, medico, data_consulta, horario_consulta, cpf)

        assert resultado == mock_query.return_value

    
    @patch('modules.db.pesquisar_receita')
    def test_botão_pesquisar_receita_campos_vazios(self,mock_query):
        # Defina a resposta que você espera do banco de dados
        tree = None
        medico = ''
        data_consulta = ''
        horario_consulta = ''
        cpf = '858.816.885-51'

        mock_query.return_value = 'Preencha pelo menos os campos : Médico, Data da consulta e horário por favor!'
        
        resultado = pesquisar_receita(tree, medico, data_consulta, horario_consulta, cpf)

        assert resultado == mock_query.return_value

    
    @patch('modules.db.pesquisar_receita')
    def test_botão_pesquisar_receita_data_invalida(self,mock_query):
        # Defina a resposta que você espera do banco de dados
        tree = None
        medico = 'Ana Clara Souza'
        data_consulta = '2024-01-00'
        horario_consulta = '15:00:00'
        cpf = '858.816.885-51'

        mock_query.return_value = 'Insira a data no formato correto (DD/MM/YYYY)!'
        
        resultado = pesquisar_receita(tree, medico, data_consulta, horario_consulta, cpf)

        assert resultado == mock_query.return_value


    @patch('modules.db.pesquisar_receita')
    def test_botão_pesquisar_receita_nao_encontrada(self,mock_query):
        # Defina a resposta que você espera do banco de dados
        tree = None
        medico = 'Natã Silva Pinto'
        data_consulta = '15/10/2024'
        horario_consulta = '11:00:00'
        cpf = '858.816.885-51'

        mock_query.return_value = 'Procuramos pelos seus filtros e não foi encontrado nenhuma receita!'
        
        resultado = pesquisar_receita(tree, medico, data_consulta, horario_consulta, cpf)

        assert resultado == mock_query.return_value

class TestBotaoAtualizarReceita(unittest.TestCase):

    print('############### TESTES DE INTEGRAÇÃO - Botão de Atualizar na tela de Receita ############################')

    @patch('modules.db.update_receita')
    def test_botão_atualizar_receita(self,mock_query):
        # Defina a resposta que você espera do banco de dados
        #Obs: Não foi possível realizar o teste nessa classe
        tree = None
        medico = 'Roberto Passos Santos'
        atestado = 'Atestado de 1 dia'
        medicamento = 'Dorflex'
        descricao = 'Paciente com muitas dores'
        data_consulta = '02/10/2024'
        horario_consulta = '09:00:00'
        cpf = '858.816.885-51'

        '''mock_query = pd.DataFrame([{'cpf': cpf, 'senha': senha}])
        mock_query.return_value = mock_query.to_string(index=False)
        
        resultado = update_receita(tree, cpf, medico, atestado, medicamento, descricao, data_consulta, horario_consulta)
        resultado = resultado[['cpf','senha']]
        resultado = resultado.to_string(index=False)

        assert resultado == mock_query.return_value'''

class TestBotaoDeletarReceita(unittest.TestCase):

    print('############### TESTES DE INTEGRAÇÃO - Botão de Deletar na tela de Receita ############################')

    @patch('modules.db.deletar_receita')
    def test_botão_deletar_receita(self,mock_query):
        # Defina a resposta que você espera do banco de dados
        #Obs: Não foi possível realizar o teste nessa classe
        tree = None
        nome = 'Jurandir Rosa Martins'
        medico = 'Matheus Garcia Lopes'
        atestado = 'Atestado de 2 dias'
        medicamento = 'Dorflex'
        descricao = 'Para dor leve a moderada'
        data_consulta = '01/01/2024'
        horario_consulta = '09:00:00'
        cpf = '858.816.885-51'

        '''mock_query = pd.DataFrame([{'cpf': cpf, 'senha': senha}])
        mock_query.return_value = mock_query.to_string(index=False)
        
        resultado = deletar_receita(tree, nome, medico, medicamento, atestado, descricao, data_consulta, horario_consulta, cpf)
        resultado = resultado[['cpf','senha']]
        resultado = resultado.to_string(index=False)

        assert resultado == mock_query.return_value'''



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

    
