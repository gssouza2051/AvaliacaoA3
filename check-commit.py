import git
import os
import sys

def check_commit_message(repo_path, keywords):
    repo = git.Repo(repo_path)
    commits = list(repo.iter_commits('HEAD'))
    palavra_chave = False

    for commit in commits:
        for keyword in keywords:
            if keyword in commit.message:
                print(f"Commit {commit.hexsha} contém a palavra-chave: {keyword}")
                palavra_chave = True
                break
            else:
                print(f"Commit {commit.hexsha} não contém nenhuma das palavras-chave!")
    if palavra_chave == False:
        sys.exit()
    

# Exemplo de uso:
repo_path = os.getcwd()
keywords = ['feat', 'fix', 'docs','refactor', 'test', 'chore', 'style']
check_commit_message(repo_path, keywords)