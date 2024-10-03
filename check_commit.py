import sys

def check_commit_message(message):
    message = sys.stdin.read().strip()
    keywords = ["fix", "feat", "chore", "docs", "refactor", "test", "style"]
    for keyword in keywords:
        if keyword in message:
            return True
    return False

if __name__ == "__main__":
    message = sys.argv[1]
    if not check_commit_message(message):
        print("A mensagem do commit precisa conter uma das palavras-chave: fix, feat, chore, docs, refactor, test, style.")
        sys.exit(1)