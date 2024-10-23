import unittest
import re
from unittest.mock import patch
from modules.format_variables import *  # Importe a função do seu módulo

# Como executar os testes
# python -m unittest testes_unitarios.py


class TestFormatCPF(unittest.TestCase):

    print('############### TESTES UNITÁRIOS RELACIONADOS A FORMATAÇÃO DE CPF ############################')

    def test_cpf_valido(self):
        cpf = '12345678909'
        resultado = format_cpf(cpf)
        self.assertEqual(resultado, '123.456.789-09')

    def test_cpf_invalido_caracteres(self):
        cpf = '123a4567890'
        self.assertFalse(format_cpf(cpf))

    def test_cpf_mais_de_11_digitos(self):
        cpf = '123456789098'
        resultado = format_cpf(cpf)
        self.assertEqual(resultado, '123.456.789-09')  # Verifica se foi limitado a 11 dígitos

    def test_cpf_menos_de_11_digitos(self):
        cpf = '1234567'
        self.assertFalse(format_cpf(cpf))

    def test_cpf_sem_formatacao(self):
        cpf = '12345678909'
        resultado = format_cpf(cpf)
        self.assertEqual(resultado, '123.456.789-09')

    def test_cpf_formatacao_incorreta(self):
        cpf = '12.345.6789-09'
        resultado = format_cpf(cpf)
        self.assertEqual(resultado, '123.456.789-09')



class TestFormatData(unittest.TestCase):

    print('############### TESTES UNITÁRIOS RELACIONADOS A VALIDAÇÃO DE DATA  ############################')

    def test_data_valida(self):
        data = '31/12/2023'
        resultado = format_data(data)
        self.assertEqual(resultado, '31/12/2023')

    def test_data_invalida_formato(self):
        data = '2023-12-31'
        resultado = format_data(data)
        self.assertFalse(resultado)

    def test_data_vazia(self):
        data = ''
        resultado = format_data(data)
        self.assertFalse(resultado)

    def test_data_nula(self):
        data = None
        resultado = format_data(data)
        self.assertFalse(resultado)

    def test_excecao_valueerror(self):
        data = '31/13/2023'
        resultado = format_data(data)
        self.assertFalse(resultado)



class TestFormatTelefone(unittest.TestCase):

    print('############### TESTES UNITÁRIOS RELACIONADOS A VALIDAÇÃO DO NÚMERO DE TELEFONE ############################')

    def test_formato_padrao_10_digitos(self):
        telefone = '11987654321'
        resultado = format_telefone(telefone)
        self.assertEqual(resultado, '(11) 98765-4321')

    def test_formato_padrao_11_digitos(self):
        telefone = '911987654321'
        resultado = format_telefone(telefone)
        self.assertEqual(resultado, '(91) 19876-54321')

    def test_formato_alternativo(self):
        telefone = '11987654321'
        resultado = format_telefone(telefone)
        self.assertEqual(resultado, '(11) 98765-4321')

    def test_numero_invalido_tamanho(self):
        telefone = '12345678'
        resultado = format_telefone(telefone)
        self.assertFalse(resultado)

    def test_numero_invalido_caracteres(self):
        telefone = '11-98765-4321a'
        resultado = format_telefone(telefone)
        self.assertEqual(resultado, '(11) 98765-4321')


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