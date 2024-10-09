#.\venv\Scripts\activate 
#deactivate

import customtkinter
from time import sleep

appearance_mode = "light"  # Variável global

def config():
    customtkinter.set_appearance_mode('dark')
    customtkinter.set_default_color_theme('dark-blue')
    janela = customtkinter.CTk()
    janela.geometry('900x700')
    return janela

def change_appearance_mode():
    global appearance_mode
    appearance_mode = "dark" if appearance_mode == "light" else "light"
    customtkinter.set_appearance_mode(appearance_mode)

def criar_conta():

    # Ocultar tela principal
    #tela_principal.pack_forget()

    # Cria uma nova janela para o cadastro
    janela_cadastro = customtkinter.CTkToplevel()
    janela_cadastro.geometry('900x700')
    janela_cadastro.title("Criar Conta")

    button_appearance_mode = customtkinter.CTkButton(master=janela_cadastro, text="Mudar Tema", command=change_appearance_mode)
    button_appearance_mode.pack(pady=5, padx=5)
    button_appearance_mode.place(relx=1.0, rely=0, x=-5, y=5, anchor="ne")
    

    # Campos de cadastro 
    nome_label = customtkinter.CTkLabel(janela_cadastro, text="Nome:")
    nome_entry = customtkinter.CTkEntry(janela_cadastro)
    email_label = customtkinter.CTkLabel(janela_cadastro, text="E-mail:")
    email_entry = customtkinter.CTkEntry(janela_cadastro)
    cpf_label = customtkinter.CTkLabel(janela_cadastro, text="CPF:")
    cpf_entry = customtkinter.CTkEntry(janela_cadastro, placeholder_text="___.___.___-__")
    telefone_label = customtkinter.CTkLabel(janela_cadastro, text="Telefone:")
    telefone_entry = customtkinter.CTkEntry(janela_cadastro, placeholder_text="(___) _____-____")
    data_nascimento_label = customtkinter.CTkLabel(janela_cadastro, text="Data de Nascimento:")
    data_nascimento_entry = customtkinter.CTkEntry(janela_cadastro, placeholder_text="DD/MM/AAAA")
    senha_label = customtkinter.CTkLabel(janela_cadastro, text="Senha:")
    senha_entry = customtkinter.CTkEntry(janela_cadastro, show="*")

    def cadastrar_usuario(janela_cadastro):
        # Aqui você colocaria a lógica para salvar os dados do usuário
        nome = nome_entry.get()
        email = email_entry.get()
        cpf = cpf_entry.get()
        telefone = telefone_entry.get()
        data_nascimento = data_nascimento_entry.get()
        senha = senha_entry.get()
        if not nome or not email or not cpf or not telefone or not data_nascimento or not senha:
            # Exibir uma mensagem de erro se algum campo estiver vazio
            print('vazio')
            label_mensagem = customtkinter.CTkLabel(janela_cadastro, text="Erro, Por favor, preencha todos os campos.", font=("Arial", 12))
            label_mensagem.pack(pady=10)
        else:
            print(f"Nome: {nome}, Email: {email}, CPF: {cpf}, Telefone: {telefone}, Dt_nascimento: {data_nascimento}, Senha: {senha}")  # Exemplo simples de impressão


    # Botão para enviar os dados
    botao_cadastrar = customtkinter.CTkButton(janela_cadastro, text="Cadastrar", command=lambda: [cadastrar_usuario(janela_cadastro), janela_cadastro.withdraw(), janela_login(config())])

    # Posicionando os elementos na janela
    nome_label.pack(pady=10)
    nome_entry.pack(pady=10)
    email_label.pack(pady=10)
    email_entry.pack(pady=10)
    cpf_label.pack(pady=10)
    cpf_entry.pack(pady=10)
    telefone_label.pack(pady=10)
    telefone_entry.pack(pady=10)
    data_nascimento_label.pack(pady=10)
    data_nascimento_entry.pack(pady=10)
    senha_label.pack(pady=10)
    senha_entry.pack(pady=10)
    botao_cadastrar.pack(pady=10)


def login(janela, cpf_valor, senha_valor):
    if not cpf_valor or not senha_valor:
        # Exibir uma mensagem de erro se algum campo estiver vazio
        label_mensagem = customtkinter.CTkLabel(janela, text="Erro, Por favor, preencha todos os campos.", font=("Arial", 12))
        label_mensagem.pack(pady=10)
    else:
        # Continuar com a lógica de login
        print("CPF:", cpf_valor)
        print("Senha:", senha_valor)
        label_mensagem = customtkinter.CTkLabel(janela, text="Login feito!", font=("Arial", 12))
        label_mensagem.pack(pady=10)
        print(f'Usuario :{cpf_valor}')
        print(f'Senha :{senha_valor}')

def janela_login(janela):


    button_appearance_mode = customtkinter.CTkButton(master=janela, text="Mudar Tema", command=change_appearance_mode)
    button_appearance_mode.pack(pady=5, padx=5)
    button_appearance_mode.place(relx=1.0, rely=0, x=-5, y=5, anchor="ne")

    def login_click():
        cpf_valor = cpf.get()
        senha_valor = senha.get()
        login(janela, cpf_valor, senha_valor)  # Chamando a função login com os valores

    texto = customtkinter.CTkLabel(janela, text='Fazer Login')
    texto.pack(padx=10,pady=10)

    cpf = customtkinter.CTkEntry(janela, placeholder_text='Seu CPF')
    cpf.pack(padx=10,pady=10)

    senha = customtkinter.CTkEntry(janela, placeholder_text='Sua senha', show='*')
    senha.pack(padx=10,pady=10)

    checkbox = customtkinter.CTkCheckBox(janela, text='Lembrar Login')
    checkbox.pack(padx=10,pady=10)

    # Botão para criar conta na tela principal
    botao_criar_conta = customtkinter.CTkButton(janela, text="Criar Conta", command=lambda: [criar_conta(), janela.withdraw()])
    botao_criar_conta.pack(pady=10)
    

    botao = customtkinter.CTkButton(janela, text='Login', command=login_click)
    botao.pack(padx=10,pady=10)
    janela.mainloop()


