# bibliotecas
import json
import sys
import os

PATH_CREDENCIAIS = rf'{os.getcwd()}/modules/credenciais.json'

def obter_credencial(service, autentication):
    # Faz a leitura do arquivo json, retorna as credenciais necessárias para conectar ao Banco de Dados

    try:
        with open(PATH_CREDENCIAIS, encoding='utf-8') as credenciais_json:
            acesso = json.load(credenciais_json)
        chave = str(acesso['{}'.format(service)]['{}'.format(autentication)])
    except Exception as e:
        print(f'Erro na credencial: {e}')
        sys.exit()
    return chave
