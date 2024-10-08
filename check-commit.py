import git
import os
import sys

def check_commit_message(repo_path, keywords):
    repo = git.Repo(repo_path)
    last_commit = repo.head.commit
    palavra_chave = False

    for keyword in keywords:
        if keyword in last_commit.message:
            print(f"Commit {last_commit.hexsha} contém a palavra-chave: {keyword}")
            palavra_chave = True  # Encontramos a palavra-chave, podemos sair da função

    if palavra_chave == False:
        print(f"O último commit {last_commit.hexsha} não contém nenhuma das palavras-chave!")

    

# Exemplo de uso:
repo_path = os.getcwd()
keywords = ['feat', 'fix', 'docs','refactor', 'test', 'chore', 'style']

'''
Conventional Commits

1.feat: -> Adição de uma nova funcionalidade
2.fix: -> Correção de um bug
3.docs: -> Alterações na documentação
4.style: -> Melhorias que não afetam o significado do código
5.refactor: -> Refatoração de código existente
6.test: -> Adição ou modificação de testes
7.chore: -> Tarefas de manutenção,ajustes na configuração,etc.'''

check_commit_message(repo_path, keywords)