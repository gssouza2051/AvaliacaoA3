import customtkinter as ctk
from datetime import datetime
import re

def format_cpf(cpf_entry):
    cpf = cpf_entry.get().replace('.', '').replace('-', '')  # Remove formatação existente
    if not cpf.isdigit():
        print("CPF inválido: somente números são permitidos.")
        return False
    cpf = cpf[:11]  # Limita a 11 dígitos
    
    if len(cpf) > 0:
        cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        cpf_entry.delete(0, 'end')
        cpf_entry.insert(0, cpf)
    else:
        return False
    return cpf


def format_data(data):
    data = data.get()
    try:
        # Converte a string para um objeto datetime
        data = datetime.strptime(data, '%d/%m/%Y')

        # Formata a data no formato desejado
        data_formatada = data.strftime('%d/%m/%Y')
        return data_formatada
    
    except ValueError:
        print("Formato de data inválido. Use DD/MM/YYYY")
        return False
    

def format_telefone(telefone):
    telefone = telefone.get()
    #Formata um número de telefone no formato (DDD) XXXXX-XXXX.

    # Remove todos os caracteres não numéricos
    telefone = re.sub(r'\D', '', telefone)

    # Verifica se o número tem pelo menos 10 dígitos
    if len(telefone) < 10:
        print('Número de telefone inválido.')
        return False

    # Formata o número
    telefone_formatado = f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"

    return telefone_formatado



def valida_email(email):
    email = email.get()
    # Valida um endereço de e-mail usando uma expressão regular básica.

    padrao_email = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(padrao_email, email):
        print('Email válido!')
        return True
    else:
        print('Email inválido!')
        return False

    
def valida_senha(senha):
    senha = senha.get()
    #Valida uma senha com base em critérios específicos.

    # Padrões para verificar a presença de:
    # - Pelo menos uma letra maiúscula
    # - Pelo menos um número
    # - Pelo menos um caractere especial (pode ser personalizado)
    # - Pelo menos 8 caracteres
    padrao = r"^(?=.*[A-Z])(?=.*\d)(?=.*[@$#./!%*#?&])[A-Za-z\d@$!%*#./?&]{8,}$"

    # Verifica se a senha corresponde ao padrão
    if re.match(padrao, senha):
        return True
    else:
        return False


