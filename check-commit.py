import git
import os

def check_commit_message(repo_path, keywords):
    repo = git.Repo(repo_path)
    commits = list(repo.iter_commits('HEAD'))

    for commit in commits:
        for keyword in keywords:
            if keyword in commit.message:
                print(f"Commit {commit.hexsha} contém a palavra-chave: {keyword}")
            else:
                print(f"Commit {commit.hexsha} não contém nenhuma das palavras-chave!")

# Exemplo de uso:
repo_path = os.getcwd()
keywords = ['feat', 'fix', 'docs','refactor', 'test', 'chore', 'style']
check_commit_message(repo_path, keywords)