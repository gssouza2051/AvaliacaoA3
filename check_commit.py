import sys

def check_commit_message(message):
    # Verifique se a mensagem contém palavras-chave proibidas
    prohibited_words = ["bloqueio", "de", "palavras", "fora", "dos", "padroes", "dos", "commits"]
    for word in prohibited_words:
        if word in message:
            return False
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: check_commit.py <mensagem_do_commit>")
        sys.exit(1)
    message = sys.argv[1]
    if not check_commit_message(message):
        print("A mensagem do commit contém palavras proibidas. Por favor, revise.")
        sys.exit(1)