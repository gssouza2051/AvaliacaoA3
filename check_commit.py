import sys

def check_commit_message(message):
    # Lista de palavras-chave obrigatórias
    keywords = ["feat", "fix", "docs", "style", "refactor", "test", "chore"]
    # ... (sua lógica de verificação aqui)
    return True  # Retorna True se a mensagem estiver OK, False caso contrário

if __name__ == "__main__":
    message = sys.argv[1]
    print(f'messagem:{message}')
    if not check_commit_message(message):
        print("Mensagem de commit inválida: use palavras-chave como 'feat', 'fix', etc.")
        sys.exit(1)