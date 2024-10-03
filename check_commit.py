import sys

def check_commit_message(message):
    # Lista de palavras-chave obrigatórias (ignorando case)
    keywords = ["feat", "fix", "docs", "style", "refactor", "test", "chore"]
    for keyword in keywords:
        if keyword.lower() == message.lower():
            return True
    return False

if __name__ == "__main__":
    message = sys.argv[1]
    mensagem = check_commit_message(message)
    if mensagem == False:
        print("Mensagem de commit inválida: use palavras-chave como 'feat', 'fix', etc.")
        sys.exit(1)