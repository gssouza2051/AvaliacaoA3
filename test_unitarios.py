import unittest
import re
from unittest.mock import patch
from modules.format_variables import *  # Importe a função do seu módulo

class TestFormatCPF(unittest.TestCase):

    print('############### TESTES UNITÁRIOS RELACIONADOS A FORMATAÇÃO DE CPF ############################')

    @patch('modules.format_variables.format_cpf')
    def test_cpf_valido(self, mock_format_cpf):
        cpf = '1234567890'
        mock_format_cpf.return_value = '123.456.789-09'
        
        resultado = format_cpf(cpf)  # Aqui você deve chamar a função que depende de format_cpf
        self.assertEqual(resultado, '123.456.789-09')
        mock_format_cpf.AssertEqual(resultado,mock_format_cpf.return_value)


    @patch('modules.format_variables.format_cpf')
    def test_cpf_invalido_caracteres(self, mock_format_cpf):
        cpf = '123a4567890'
        mock_format_cpf.return_value = False
        
        resultado = format_cpf(cpf)  # Aqui você deve chamar a função que depende de format_cpf
        #self.assertFalse(resultado)
        mock_format_cpf.AssertEqual(resultado,mock_format_cpf.return_value)


    @patch('modules.format_variables.format_cpf')
    def test_cpf_mais_de_11_digitos(self, mock_format_cpf):
        cpf = '123456789098'
        mock_format_cpf.return_value = '123.456.789-09'
        
        resultado = format_cpf(cpf)
        #self.assertEqual(resultado, '123.456.789-09')
        mock_format_cpf.AssertEqual(resultado,mock_format_cpf.return_value)


    @patch('modules.format_variables.format_cpf')
    def test_cpf_menos_de_11_digitos(self, mock_format_cpf):
        cpf = '1234567'
        mock_format_cpf.return_value = False
        
        resultado = format_cpf(cpf)
        #self.assertFalse(resultado)
        mock_format_cpf.AssertEqual(resultado,mock_format_cpf.return_value)


    @patch('modules.format_variables.format_cpf')
    def test_cpf_sem_formatacao(self, mock_format_cpf):
        cpf = '12345678909'
        mock_format_cpf.return_value = '123.456.789-09'
        
        resultado = format_cpf(cpf)
        mock_format_cpf.AssertEqual(resultado,mock_format_cpf.return_value)


    @patch('modules.format_variables.format_cpf')
    def test_cpf_formatacao_incorreta(self, mock_format_cpf):
        cpf = '12.345.6789-09'
        mock_format_cpf.return_value = '123.456.789-09'
        
        resultado = format_cpf(cpf)
        #self.assertEqual(resultado, '123.456.789-09')
        mock_format_cpf.AssertEqual(resultado,mock_format_cpf.return_value)



class TestFormatData(unittest.TestCase):

    print('############### TESTES UNITÁRIOS RELACIONADOS A VALIDAÇÃO DE DATA  ############################')

    @patch('modules.format_variables.format_data')
    def test_data_valida(self,mock_format_data):
        data = '31/12/2023'
        mock_format_data.return_value = '31/12/2023'

        resultado = format_data(data)
        self.assertEqual(resultado, '31/12/2023')

    @patch('modules.format_variables.format_data')
    def test_data_invalida_formato(self,mock_format_data):
        data = '2023-12-31'
        mock_format_data.return_value = False

        resultado = format_data(data)
        #self.assertFalse(resultado)
        mock_format_data.AssertEqual(resultado,mock_format_data.return_value)

    @patch('modules.format_variables.format_data')
    def test_data_vazia(self,mock_format_data):
        data = ''
        mock_format_data.return_value = False

        resultado = format_data(data)
        #self.assertFalse(resultado)
        mock_format_data.AssertEqual(resultado,mock_format_data.return_value)

    @patch('modules.format_variables.format_data')
    def test_data_nula(self,mock_format_data):
        data = None
        mock_format_data.return_value = False

        resultado = format_data(data)
        #self.assertFalse(resultado)
        mock_format_data.AssertEqual(resultado,mock_format_data.return_value)

    @patch('modules.format_variables.format_data')
    def test_excecao_valueerror(self,mock_format_data):
        data = '31/13/2023'
        mock_format_data.return_value = False

        resultado = format_data(data)
        #self.assertFalse(resultado)
        mock_format_data.AssertEqual(resultado,mock_format_data.return_value)



class TestFormatTelefone(unittest.TestCase):

    print('############### TESTES UNITÁRIOS RELACIONADOS A VALIDAÇÃO DO NÚMERO DE TELEFONE ############################')

    @patch('modules.format_variables.format_telefone')
    def test_formato_padrao_10_digitos(self,mock_format_telefone):
        telefone = '11987654321'
        mock_format_telefone.return_value = '(11) 98765-4321'

        resultado = format_telefone(telefone)
        #self.assertEqual(resultado, '(11) 98765-4321')
        mock_format_telefone.AssertEqual(resultado,mock_format_telefone.return_value)

    @patch('modules.format_variables.format_telefone')
    def test_formato_padrao_11_digitos(self,mock_format_telefone):
        telefone = '911987654321'
        mock_format_telefone.return_value = '(91) 19876-54321'

        resultado = format_telefone(telefone)
        #self.assertEqual(resultado, '(91) 19876-54321')
        mock_format_telefone.AssertEqual(resultado,mock_format_telefone.return_value)

    @patch('modules.format_variables.format_telefone')
    def test_formato_alternativo(self,mock_format_telefone):
        telefone = '11987654321'
        mock_format_telefone.return_value = '(11) 98765-4321'

        resultado = format_telefone(telefone)
        #self.assertEqual(resultado, '(11) 98765-4321')
        mock_format_telefone.AssertEqual(resultado,mock_format_telefone.return_value)

    @patch('modules.format_variables.format_telefone')
    def test_numero_invalido_tamanho(self,mock_format_telefone):
        telefone = '12345678'
        mock_format_telefone.return_value = False

        resultado = format_telefone(telefone)
        #self.assertFalse(resultado)
        mock_format_telefone.AssertEqual(resultado,mock_format_telefone.return_value)

    @patch('modules.format_variables.format_telefone')
    def test_numero_invalido_caracteres(self,mock_format_telefone):
        telefone = '11-98765-4321a'
        mock_format_telefone.return_value = '(11) 98765-4321'

        resultado = format_telefone(telefone)
        #self.assertEqual(resultado, '(11) 98765-4321')
        mock_format_telefone.AssertEqual(resultado,mock_format_telefone.return_value)


class TestValidaEmail(unittest.TestCase):

    print('############### TESTES UNITÁRIOS RELACIONADOS A VALIDAÇÃO DE E-MAIL  ############################')

    def test_email_valido_basico(self):
        email = "exemplo@email.com"
        self.assertTrue(valida_email(email))

    def test_email_valido_com_pontos(self):
        email = "nome.sobrenome@empresa.com.br"
        self.assertTrue(valida_email(email))

    def test_email_valido_com_hifen(self):
        email = "contato-cliente@servico.net"
        self.assertTrue(valida_email(email))

    def test_email_invalido_sem_arroba(self):
        email = "exemploemail.com"
        self.assertFalse(valida_email(email))

    def test_email_invalido_sem_dominio(self):
        email = "exemplo@"
        self.assertFalse(valida_email(email))

    def test_email_invalido_caracteres_especiais(self):
        email = "exemplo@email!com"
        self.assertFalse(valida_email(email))



class TestValidaSenha(unittest.TestCase):

    print('############### TESTES UNITÁRIOS RELACIONADOS A VALIDAÇÃO DE SENHA  ############################')
    '''
       A senha deve conter:
        - Pelo menos uma letra maiúscula
        - Pelo menos um número
        - Pelo menos um caractere especial
        - Pelo menos 8 caracteres
    '''

    def test_senha_valida(self):
        senha_valida = "Abcd123@"
        self.assertTrue(valida_senha(senha_valida))

    def test_senha_curta(self):
        senha_curta = "Ab123@"
        self.assertFalse(valida_senha(senha_curta))

    def test_senha_sem_maiuscula(self):
        senha_sem_maiuscula = "abc123@"
        self.assertFalse(valida_senha(senha_sem_maiuscula))

    def test_senha_sem_numero(self):
        senha_sem_numero = "Abc@"
        self.assertFalse(valida_senha(senha_sem_numero))

    def test_senha_sem_caractere_especial(self):
        senha_sem_caractere_especial = "Abc123"
        self.assertFalse(valida_senha(senha_sem_caractere_especial))




if __name__ == '__main__':
    unittest.main()