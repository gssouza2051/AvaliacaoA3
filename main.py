import tkinter as tk
#from modules import page
from modules import db

def main():
    conn = db.conecta_db()

    base_usuarios = db.realiza_consulta_db( 'select * from saude.tbl_usuarios', conn)
    print(f'\nBase usuarios :\n{base_usuarios}')

    base_medicos = db.realiza_consulta_db( 'select * from saude.tbl_medicos', conn)
    print(f'\nBase médicos :\n{base_medicos}')

    base_pacientes = db.realiza_consulta_db( 'select * from saude.tbl_pacientes', conn)
    print(f'\nBase pacientes :\n{base_pacientes}')

    base_consultas = db.realiza_consulta_db( 'select * from saude.tbl_consultas', conn)
    print(f'\nBase consultas :\n{base_consultas}')

    base_atestados = db.realiza_consulta_db( 'select * from saude.tbl_atestados', conn)
    print(f'\nBase atestados :\n{base_atestados}')



main()










'''def verificar_login():
    usuario = entrada_usuario.get()
    senha = entrada_senha.get()

    # Substitua por sua lógica de verificação de credenciais
    if usuario == "gabriel" and senha == "9090":
        mensagem.config(text="Login bem-sucedido!")
    else:
        mensagem.config(text="Usuário ou senha inválidos.")

# Cria a janela principal
janela = tk.Tk()
janela.title("Tela de Login")

# Define as dimensões da janela (800 pixels de largura por 600 pixels de altura)
janela.geometry("800x600")

# Cria os labels e campos de entrada
label_usuario = tk.Label(janela, text="Usuário:")
label_usuario.pack()
entrada_usuario = tk.Entry(janela)
entrada_usuario.pack()

label_senha = tk.Label(janela, text="Senha:")
label_senha.pack()
entrada_senha = tk.Entry(janela, show="*")  # Mostra asteriscos no lugar da senha
entrada_senha.pack()

# Cria o botão
botao_login = tk.Button(janela, text="Login", command=verificar_login)
botao_login.pack()

# Cria um label para exibir mensagens
mensagem = tk.Label(janela, text="")
mensagem.pack()

janela.mainloop()'''