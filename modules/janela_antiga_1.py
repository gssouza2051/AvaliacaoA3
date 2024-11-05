#.\venv\Scripts\activate 
#deactivate
# pip install -r requirements

import customtkinter as ctk
from tkinter import ttk,messagebox
import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime
from modules import format_variables as format
from time import sleep
import pandas as pd
from modules import db


appearance_mode = "light"  # Variável global
global imagem

def config():
    ctk.set_appearance_mode('light')
    ctk.set_default_color_theme('dark-blue')
    janela = ctk.CTk()
    janela.geometry('900x700')
    janela.resizable(False, False)
    return janela



def change_appearance_mode():
    global appearance_mode
    appearance_mode = "dark" if appearance_mode == "light" else "light"
    ctk.set_appearance_mode(appearance_mode)

def janela_criar_conta():

    # Cria uma nova janela para o cadastro
    janela_cadastro = ctk.CTkToplevel(fg_color='#03dffc')
    janela_cadastro.geometry('900x700')
    janela_cadastro.resizable(False, False)
    janela_cadastro.title("Criar Conta")

    image_path = r".\midia/template.png"
    image = ctk.CTkImage(light_image= Image.open(image_path), size=(900,200))  # Redimensionar a imagem para o tamanho da janela
    image_label = ctk.CTkLabel(janela_cadastro, image=image, text="")
    image_label.place(x = 0, y =0)

    button_appearance_mode = ctk.CTkButton(master=janela_cadastro, text="Mudar Tema", command=change_appearance_mode, hover_color='green')
    button_appearance_mode.pack(pady=5, padx=5)
    button_appearance_mode.place(relx=1.0, rely=0, x=-5, y=5, anchor="ne")
    

    # Campos de cadastro 
    nome_label = ctk.CTkLabel(janela_cadastro, text="Nome:", text_color='black')
    nome_entry = ctk.CTkEntry(janela_cadastro)
    email_label = ctk.CTkLabel(janela_cadastro, text="E-mail:", text_color='black')
    email_entry = ctk.CTkEntry(janela_cadastro, placeholder_text='seu_email@exemplo.com',width=160)
    cpf_label = ctk.CTkLabel(janela_cadastro, text="CPF:", text_color='black')
    cpf_entry = ctk.CTkEntry(janela_cadastro, placeholder_text="___.___.___-__")
    #cpf_entry.bind("<KeyRelease>", format.format_cpf(cpf_entry))  # Associa a função ao evento de soltar a tecla
    telefone_label = ctk.CTkLabel(janela_cadastro, text="Telefone:", text_color='black')
    telefone_entry = ctk.CTkEntry(janela_cadastro, placeholder_text="(___) _____-____")
    data_nascimento_label = ctk.CTkLabel(janela_cadastro, text="Data de Nascimento:", text_color='black')
    data_nascimento_entry = ctk.CTkEntry(janela_cadastro, placeholder_text="DD/MM/AAAA")
    senha_label = ctk.CTkLabel(janela_cadastro, text="Senha:", text_color='black')
    senha_requisitos = ctk.CTkLabel(janela_cadastro, text="A senha deve conter:", text_color='black')
    senha_requisitos1 = ctk.CTkLabel(janela_cadastro, text="- Pelo menos uma letra maiúscula", text_color='black')
    senha_requisitos2 = ctk.CTkLabel(janela_cadastro, text="- Pelo menos um número", text_color='black')
    senha_requisitos3 = ctk.CTkLabel(janela_cadastro, text="- Pelo menos um caractere especial", text_color='black')
    senha_requisitos4 = ctk.CTkLabel(janela_cadastro, text="- Pelo menos 8 caracteres", text_color='black')
                                    
    senha_entry = ctk.CTkEntry(janela_cadastro, show="*")

    def cadastrar_usuario(janela_cadastro):
        print('\n')
        # Aqui você colocaria a lógica para salvar os dados do usuário
        nome = nome_entry.get()
        print(f'nome :{nome}')
        email = email_entry.get()
        print(f'email :{email}')
        verifica_email = format.valida_email(email_entry)

        cpf = format.format_cpf(cpf_entry)
        print(f'cpf :{cpf}')

        telefone = format.format_telefone(telefone_entry)
        print(f'telefone :{telefone}')

        data_nascimento = format.format_data(data_nascimento_entry)
        print(f'dt_nascimento :{data_nascimento}')

        senha = senha_entry.get()
        print(f'senha :{senha}')
        valida_senha = format.valida_senha(senha_entry)

        if nome == '' or email == '' or  cpf == '' or telefone == '' or data_nascimento == '' or senha == '':

            # Exibir uma mensagem de erro se algum campo estiver vazio
            print('Preencha os campos necessários.')
            label_mensagem = ctk.CTkLabel(janela_cadastro, text="Erro!! Por favor, preencha todos os campos.", font=("Arial", 12), bg_color='#fc031c', text_color='black')
            #label_mensagem.pack(padx=10,pady=10, anchor="w")
            label_mensagem.place(x=310, y=620)
            # Após 2 segundos, remove a label da tela
            janela_cadastro.after(2000, label_mensagem.destroy)
            #janela_cadastro.withdraw()
        
        elif verifica_email == False or valida_senha == False or data_nascimento == False or telefone == False or cpf == False:

            # Exibir uma mensagem de erro se algum campo estiver fora do padrão necessário
            print('Algum campo está fora do padrão necessário')
            label_mensagem = ctk.CTkLabel(janela_cadastro, text="Erro!! Por favor, preencha todos os campos no formato correto", font=("Arial", 12), bg_color='#fc031c', text_color='black')
            label_mensagem.place(x=310, y=620)
            # Após 2 segundos, remove a label da tela
            janela_cadastro.after(2000, label_mensagem.destroy)
            #janela_cadastro.withdraw()
            
        else:
            # Botão para enviar os dados
            print(f"Nome: {nome}, Email: {email}, CPF: {cpf}, Telefone: {telefone}, Dt_nascimento: {data_nascimento}, Senha: {senha}")  # Exemplo simples de impressão
            db.cadastro_usuario(nome,email,senha,data_nascimento,telefone,cpf)
            label_mensagem = ctk.CTkLabel(janela_cadastro, text="Cadastro realizado com sucesso!!", font=("Arial", 12), bg_color='#61eb34', text_color='black')
            label_mensagem.place(x=320, y=620)
            # Após 1 segundo, remove a label da tela
            janela_cadastro.after(2000, label_mensagem.destroy)
            sleep(1)
            janela_cadastro.withdraw()
            janela_login()

    
    
    #botao_cadastrar = ctk.CTkButton(janela_cadastro, text="Cadastrar", command=lambda: [cadastrar_usuario(janela_cadastro), janela_cadastro.withdraw(), janela_login()], hover_color='green')
    botao_cadastrar = ctk.CTkButton(janela_cadastro, text="Cadastrar",command=lambda: [cadastrar_usuario(janela_cadastro)], hover_color='green')
    botao_voltar = ctk.CTkButton(janela_cadastro, text="Voltar para página de login", command=lambda: [janela_cadastro.withdraw(), janela_login()], hover_color='green', width=260, text_color='black')
    botao_voltar.place(relx=0, rely=1.0, anchor="sw")

    # Posicionando os elementos na janela
    botao_cadastrar.place(x=350, y=580)
    nome_label.place(x=100, y=210)
    nome_entry.place(x=100, y=240)
    email_label.place(x=100, y=350)
    email_entry.place(x=100, y=380)
    cpf_label.place(x=100, y=490)
    cpf_entry.place(x=100, y=520)
    telefone_label.place(x=550, y=210)
    telefone_entry.place(x=550, y=240)
    data_nascimento_label.place(x=550, y=350)
    data_nascimento_entry.place(x=550, y=380)
    senha_label.place(x=550, y=490)
    senha_entry.place(x=550, y=520)
    senha_requisitos.place(x=550, y=560)
    senha_requisitos1.place(x=550, y=580)
    senha_requisitos2.place(x=550, y=600)
    senha_requisitos3.place(x=550, y=620)
    senha_requisitos4.place(x=550, y=640)


def login(janela, cpf_valor, senha_valor):
    if cpf_valor == '' or senha_valor == '':
        # Exibir uma mensagem de erro se algum campo estiver vazio
        label_mensagem = ctk.CTkLabel(janela, text="Erro!!! Por favor, preencha todos os campos.", font=("Arial", 12), bg_color='#fc031c', text_color='black')
        label_mensagem.pack(padx=10,pady=10, anchor="w")
        # Após 2 segundos, remove a label da tela
        janela.after(2000, label_mensagem.destroy)
    else:
        # Continuar com a lógica de login

        #print(f'Usuario :{cpf_valor}')
        #print(f'Senha :{senha_valor}')

        # Faz a verificação das credenciais no banco
        login = db.pagina_login(cpf_valor, senha_valor)
        #print(login)
        if not login.empty:

            label_mensagem = ctk.CTkLabel(janela, text="Login feito!", font=("Arial", 12), bg_color='#61eb34', text_color='black')
            label_mensagem.pack(padx=10,pady=10, anchor="w")
            # Após 2 segundos, remove a label da tela
            janela.after(2000, label_mensagem.destroy)
            janela.withdraw()
            janela_principal()
        else:
            # Exibir uma mensagem de erro se login ou senha nao for encontrado
            label_mensagem = ctk.CTkLabel(janela, text="Erro!!! Login ou senha inválidos.", font=("Arial", 12), bg_color='#fc031c', text_color='black')
            label_mensagem.pack(padx=10,pady=10, anchor="w")
            # Após 2 segundos, remove a label da tela
            janela.after(4000, label_mensagem.destroy)

        

def janela_login():

    # Carregar a imagem
    janela = ctk.CTkToplevel(fg_color='#03dffc')
    janela.geometry('900x700')
    janela.resizable(False, False)

    janela.title("Tela de Login")
    image_path = r".\midia/login.png"

    image = ctk.CTkImage(light_image= Image.open(image_path), size=(900,700))  # Redimensionar a imagem para o tamanho da janela
    image_label = ctk.CTkLabel(janela, image=image, text="")
    image_label.place(x = 0, y =0)

    button_appearance_mode = ctk.CTkButton(master=janela, text="Mudar Tema", command=change_appearance_mode, hover_color='green')
    button_appearance_mode.pack(pady=5, padx=5)
    button_appearance_mode.place(relx=1.0, rely=0, x=-5, y=5, anchor="ne")

    def login_click():
        cpf_valor = cpf.get()
        senha_valor = senha.get()
        login(janela, cpf_valor, senha_valor)  # Chamando a função login com os valores

    texto = ctk.CTkLabel(janela, text='Fazer Login', bg_color='#03dffc', text_color='black')
    texto.pack(padx=50,pady=10, anchor="w")

    cpf = ctk.CTkEntry(janela, placeholder_text='Seu CPF')
    cpf.pack(padx=10,pady=10, anchor="w")

    senha = ctk.CTkEntry(janela, placeholder_text='Sua senha', show='*')
    senha.pack(padx=10,pady=10, anchor="w")

    checkbox = ctk.CTkCheckBox(janela, text='Lembrar Login', bg_color='#03dffc', text_color='black')
    checkbox.pack(padx=10,pady=10, anchor="w")

    # Botão para criar conta na tela principal
    botao_criar_conta = ctk.CTkButton(janela, text="Criar Conta", command=lambda: [janela_criar_conta(), janela.withdraw()], hover_color='green')
    botao_criar_conta.pack(padx=10,pady=10, anchor="w")
    

    botao = ctk.CTkButton(janela, text='Login', command=login_click, hover_color='green')
    botao.pack(padx=10,pady=10, anchor="w")
    janela.mainloop()


def janela_principal():

    # Cria uma nova janela para o cadastro
    janela_principal = ctk.CTkToplevel(fg_color='#03dffc')
    janela_principal.geometry('900x700')
    janela_principal.resizable(False, False)
    janela_principal.title("Saúde conectada")
    
    image_path = r".\midia/template.png"
    image = ctk.CTkImage(light_image= Image.open(image_path), size=(900,200))  # Redimensionar a imagem para o tamanho da janela
    image_label = ctk.CTkLabel(janela_principal, image=image, text="")
    image_label.place(x = 0, y =0)

    button_appearance_mode = ctk.CTkButton(master=janela_principal, text="Mudar Tema", command=change_appearance_mode, hover_color='green')
    button_appearance_mode.pack(pady=5, padx=5)
    button_appearance_mode.place(relx=1.0, rely=0, x=-5, y=5, anchor="ne")
    
    # Botões
    image_path = r".\midia/saúde.png"
    image = ctk.CTkImage(light_image= Image.open(image_path), size=(100,100))  # Redimensionar a imagem para o tamanho da janela
    image_label = ctk.CTkButton(janela_principal, image=image, text='Acompanhe seu histórico de atendimentos', command=lambda: [janela_principal.withdraw(), janela_historico_atendimentos()], compound='top', fg_color='#03dffc', text_color='black', width=260)
    image_label.place(x = 100, y =210)

    image_path = r".\midia/hospital.png"
    image = ctk.CTkImage(light_image= Image.open(image_path), size=(100,100))  # Redimensionar a imagem para o tamanho da janela
    image_label = ctk.CTkButton(janela_principal, image=image, text='Localize as unidades disponíveis', command=lambda: [janela_principal.withdraw(), janela_localiza_unidades()], compound='top', fg_color='#03dffc', text_color='black', width=260)
    image_label.place(x=100, y=350)

    image_path = r".\midia/receita.png"
    image = ctk.CTkImage(light_image= Image.open(image_path), size=(100,100))  # Redimensionar a imagem para o tamanho da janela
    image_label = ctk.CTkButton(janela_principal, image=image, text='Verifique suas ultimas receitas aqui', command=lambda: [janela_principal.withdraw(), janela_historico_receitas()], compound='top', fg_color='#03dffc', text_color='black', width=260)
    image_label.place(x=100, y=490)

    image_path = r".\midia/cartao.png"
    image = ctk.CTkImage(light_image= Image.open(image_path), size=(100,100))  # Redimensionar a imagem para o tamanho da janela
    image_label = ctk.CTkButton(janela_principal, image=image, text='Acessar cartão', command=lambda: [janela_principal.withdraw(), janela_cartao_paciente()], compound='top', fg_color='#03dffc', text_color='black', width=260)
    image_label.place(x=550, y=210)

    image_path = r".\midia/medicamento.png"
    image = ctk.CTkImage(light_image= Image.open(image_path), size=(100,100))  # Redimensionar a imagem para o tamanho da janela
    image_label = ctk.CTkButton(janela_principal, image=image, text='Disponibilidade medicamentos', command=lambda: [janela_principal.withdraw(), janela_medicamentos()], compound='top', fg_color='#03dffc', text_color='black', width=260)
    image_label.place(x=550, y=350)

    image_path = r".\midia/ouvidoria.png"
    image = ctk.CTkImage(light_image= Image.open(image_path), size=(100,100))  # Redimensionar a imagem para o tamanho da janela
    image_label = ctk.CTkButton(janela_principal, image=image, text='Ouvidoria - Saúde conectada', command=lambda: [janela_principal.withdraw(), janela_ouvidoria()], compound='top', fg_color='#03dffc', text_color='black', width=260)
    image_label.place(x=550, y=490)


    # Botão para enviar os dados
    botao_voltar = ctk.CTkButton(janela_principal, text="Voltar para página de login", command=lambda: [janela_principal.withdraw(), janela_login()], hover_color='green', width=260, text_color='black')
    botao_voltar.place(relx=0, rely=1.0, anchor="sw")

def janela_historico_atendimentos():

    # Cria uma nova janela para o histórico de atendimentos do paciente
    janela_historico_atendimentos = ctk.CTkToplevel()
    janela_historico_atendimentos.config(bg='#161C25')
    janela_historico_atendimentos.geometry('900x700')
    janela_historico_atendimentos.resizable(False, False)
    janela_historico_atendimentos.title("Histórico de atendimentos")
    
    image_path = r".\midia/template.png"
    image = ctk.CTkImage(light_image= Image.open(image_path), size=(900,200))  # Redimensionar a imagem para o tamanho da janela
    image_label = ctk.CTkLabel(janela_historico_atendimentos, image=image, text="")
    image_label.place(x = 0, y =0)

    button_appearance_mode = ctk.CTkButton(master=janela_historico_atendimentos, text="Mudar Tema", command=change_appearance_mode, hover_color='green')
    button_appearance_mode.pack(pady=5, padx=5)
    button_appearance_mode.place(relx=1.0, rely=0, x=-5, y=5, anchor="ne")

    # Criar os elementos da interface
    font1 = ('Arial',20,'bold')
    font2 = ('Arial',12,'bold')
    font3 = ('Arial',17,'bold')

    nome_label = ctk.CTkLabel(janela_historico_atendimentos, font=font1,text='Nome:',text_color='#fff',bg_color='#161C25')
    nome_label.place(x=20,y=260)

    nome_entry = ctk.CTkEntry(janela_historico_atendimentos, font=font1,text_color='#000',fg_color='#fff', border_color='#0C9295', border_width=2, width=180)
    nome_entry.place(x=100,y=260)

    plano_saude_label = ctk.CTkLabel(janela_historico_atendimentos, font=font3,text='Plano de\nsaúde:',text_color='#fff',bg_color='#161C25')
    plano_saude_label.place(x=20,y=340)

    plano_saude_entry = ctk.CTkEntry(janela_historico_atendimentos, font=font1,text_color='#000',fg_color='#fff', border_color='#0C9295', border_width=2, width=180)
    plano_saude_entry.place(x=100,y=340)

    data_consulta_label = ctk.CTkLabel(janela_historico_atendimentos, font=font3,text='Data da\nConsulta:',text_color='#fff',bg_color='#161C25')
    data_consulta_label.place(x=20,y=400)

    data_consulta_entry = ctk.CTkEntry(janela_historico_atendimentos, font=font1,text_color='#000',fg_color='#fff', border_color='#0C9295', border_width=2, width=180)
    data_consulta_entry.place(x=100,y=400)

    status_label = ctk.CTkLabel(janela_historico_atendimentos, font=font1,text='Status:',text_color='#fff',bg_color='#161C25')
    status_label.place(x=20,y=460)

    options = ['Cancelado','Realizado','Pendente']
    variable1 = str()

    genero_options = ctk.CTkComboBox(janela_historico_atendimentos, font=font1, text_color='#000',fg_color='#fff', dropdown_hover_color='#0C9295', button_color='#0C9295', button_hover_color='#0C9295',border_color='#0C9295',width=180,variable=variable1, values=options, state='readonly')
    genero_options.set('')
    genero_options.place(x=100,y=460)

    medico_label = ctk.CTkLabel(janela_historico_atendimentos, font=font1,text='Status:',text_color='#fff',bg_color='#161C25')
    medico_label.place(x=20,y=540)

    medico_entry = ctk.CTkEntry(janela_historico_atendimentos, font=font1,text_color='#000',fg_color='#fff', border_color='#0C9295', border_width=2, width=180)
    medico_entry.place(x=100,y=540)

    adicionar_botao = ctk.CTkButton(janela_historico_atendimentos,font=font1,text_color='#fff',text='Adicionar', fg_color='#05A312',hover_color='#00850B',bg_color='#161C25', cursor='hand2',corner_radius=15,width=260)
    adicionar_botao.place(x=20,y=590)

    pesquisar_botao = ctk.CTkButton(janela_historico_atendimentos,font=font1,text_color='#fff',text='Pesquisar', command=lambda: [db.pesquisar()], fg_color='#161C25',hover_color='#FF5002',bg_color='#161C25',border_color='#F15704',border_width=2,cursor='hand2',corner_radius=15,width=260)
    pesquisar_botao.place(x=20,y=630)

    atualizar_botao = ctk.CTkButton(janela_historico_atendimentos,font=font1,text_color='#fff',text='Atualizar', fg_color='#161C25',hover_color='#FF5002',bg_color='#161C25',border_color='#F15704',border_width=2,cursor='hand2',corner_radius=15,width=260)
    atualizar_botao.place(x=300,y=630)

    deletar_botao = ctk.CTkButton(janela_historico_atendimentos,font=font1,text_color='#fff',text='Deletar', fg_color='#E40404',hover_color='#AE0000',bg_color='#161C25',border_color='#E40404',border_width=2,cursor='hand2',corner_radius=15,width=260)
    deletar_botao.place(x=580,y=630)

    estilo = ttk.Style(janela_historico_atendimentos)
    estilo.theme_use('clam')
    estilo.configure('Treeview',font=font2,foreground='#fff',background='#000', fieldbackground='#313837')
    estilo.map('Treeview',background=[('selected', '#1A8F2D')])

    tree =ttk.Treeview(janela_historico_atendimentos,height=15)

    tree['columns'] = ('Médico', 'Plano', 'Horário', 'Especialidade', 'Status')

    tree.column('#0', width=0, stretch=tk.NO)
    tree.column('Médico',anchor=tk.CENTER, width=100)
    tree.column('Plano',anchor=tk.CENTER, width=120)
    tree.column('Horário',anchor=tk.CENTER, width=120)
    tree.column('Especialidade',anchor=tk.CENTER, width=120)
    tree.column('Status',anchor=tk.CENTER, width=120)

    tree.heading('Médico', text='Médico')
    tree.heading('Plano', text='Plano')
    tree.heading('Horário', text='Horário')
    tree.heading('Especialidade', text='Especialidade')
    tree.heading('Status', text='Status')

    tree.place(x=300,y=260)


    # Botão para enviar os dados
    botao_voltar = ctk.CTkButton(janela_historico_atendimentos, text="Voltar para página principal", command=lambda: [janela_historico_atendimentos.withdraw(), janela_principal()], hover_color='green', width=260, text_color='black')
    botao_voltar.place(relx=0, rely=1.0, anchor="sw")


def janela_localiza_unidades():

    # Cria uma nova janela para localizar as unidades médicas disponíveis
    janela_localiza_unidades = ctk.CTkToplevel()
    janela_localiza_unidades.config(bg='#161C25')
    janela_localiza_unidades.geometry('900x700')
    janela_localiza_unidades.resizable(False, False)
    janela_localiza_unidades.title("Unidades médicas")
    
    image_path = r".\midia/template.png"
    image = ctk.CTkImage(light_image= Image.open(image_path), size=(900,200))  # Redimensionar a imagem para o tamanho da janela
    image_label = ctk.CTkLabel(janela_localiza_unidades, image=image, text="")
    image_label.place(x = 0, y =0)

    button_appearance_mode = ctk.CTkButton(master=janela_localiza_unidades, text="Mudar Tema", command=change_appearance_mode, hover_color='green')
    button_appearance_mode.pack(pady=5, padx=5)
    button_appearance_mode.place(relx=1.0, rely=0, x=-5, y=5, anchor="ne")

    # Criar os elementos da interface
    font1 = ('Arial',20,'bold')
    font2 = ('Arial',12,'bold')

    id_label = ctk.CTkLabel(janela_localiza_unidades, font=font1,text='ID:',text_color='#fff',bg_color='#161C25')
    id_label.place(x=20,y=260)

    id_entry = ctk.CTkEntry(janela_localiza_unidades, font=font1,text_color='#000',fg_color='#fff', border_color='#0C9295', border_width=2, width=180)
    id_entry.place(x=100,y=260)

    nome_label = ctk.CTkLabel(janela_localiza_unidades, font=font1,text='Nome:',text_color='#fff',bg_color='#161C25')
    nome_label.place(x=20,y=340)

    nome_entry = ctk.CTkEntry(janela_localiza_unidades, font=font1,text_color='#000',fg_color='#fff', border_color='#0C9295', border_width=2, width=180)
    nome_entry.place(x=100,y=340)

    cargo_label = ctk.CTkLabel(janela_localiza_unidades, font=font1,text='Cargo:',text_color='#fff',bg_color='#161C25')
    cargo_label.place(x=20,y=400)

    cargo_entry = ctk.CTkEntry(janela_localiza_unidades, font=font1,text_color='#000',fg_color='#fff', border_color='#0C9295', border_width=2, width=180)
    cargo_entry.place(x=100,y=400)

    genero_label = ctk.CTkLabel(janela_localiza_unidades, font=font1,text='Gênero:',text_color='#fff',bg_color='#161C25')
    genero_label.place(x=20,y=460)

    options = ['Feminino','Masculino']
    variable1 = str()

    genero_options = ctk.CTkComboBox(janela_localiza_unidades, font=font1, text_color='#000',fg_color='#fff', dropdown_hover_color='#0C9295', button_color='#0C9295', button_hover_color='#0C9295',border_color='#0C9295',width=180,variable=variable1, values=options, state='readonly')
    genero_options.set('Male')
    genero_options.place(x=100,y=460)

    status_label = ctk.CTkLabel(janela_localiza_unidades, font=font1,text='Status:',text_color='#fff',bg_color='#161C25')
    status_label.place(x=20,y=540)

    status_entry = ctk.CTkEntry(janela_localiza_unidades, font=font1,text_color='#000',fg_color='#fff', border_color='#0C9295', border_width=2, width=180)
    status_entry.place(x=100,y=540)

    adicionar_botao = ctk.CTkButton(janela_localiza_unidades,font=font1,text_color='#fff',text='Adicionar', fg_color='#05A312',hover_color='#00850B',bg_color='#161C25', cursor='hand2',corner_radius=15,width=260)
    adicionar_botao.place(x=20,y=590)

    limpar_botao = ctk.CTkButton(janela_localiza_unidades,font=font1,text_color='#fff',text='Limpar', fg_color='#161C25',hover_color='#FF5002',bg_color='#161C25',border_color='#F15704',border_width=2,cursor='hand2',corner_radius=15,width=260)
    limpar_botao.place(x=20,y=630)

    atualizar_botao = ctk.CTkButton(janela_localiza_unidades,font=font1,text_color='#fff',text='Atualizar', fg_color='#161C25',hover_color='#FF5002',bg_color='#161C25',border_color='#F15704',border_width=2,cursor='hand2',corner_radius=15,width=260)
    atualizar_botao.place(x=300,y=630)

    deletar_botao = ctk.CTkButton(janela_localiza_unidades,font=font1,text_color='#fff',text='Deletar', fg_color='#E40404',hover_color='#AE0000',bg_color='#161C25',border_color='#E40404',border_width=2,cursor='hand2',corner_radius=15,width=260)
    deletar_botao.place(x=580,y=630)

    estilo = ttk.Style(janela_localiza_unidades)
    estilo.theme_use('clam')
    estilo.configure('Treeview',font=font2,foreground='#fff',background='#000', fieldbackground='#313837')
    estilo.map('Treeview',background=[('selected', '#1A8F2D')])

    tree =ttk.Treeview(janela_localiza_unidades,height=15)

    tree['columns'] = ('ID', 'Nome', 'Cargo', 'Genero', 'Status')

    tree.column('#0', width=0, stretch=tk.NO)
    tree.column('ID',anchor=tk.CENTER, width=100)
    tree.column('Nome',anchor=tk.CENTER, width=120)
    tree.column('Cargo',anchor=tk.CENTER, width=120)
    tree.column('Genero',anchor=tk.CENTER, width=120)
    tree.column('Status',anchor=tk.CENTER, width=120)

    tree.heading('ID', text='ID')
    tree.heading('Nome', text='Nome')
    tree.heading('Cargo', text='Cargo')
    tree.heading('Genero', text='Genero')
    tree.heading('Status', text='Status')

    tree.place(x=300,y=260)



    
    # Botão para enviar os dados
    botao_voltar = ctk.CTkButton(janela_localiza_unidades, text="Voltar para página principal", command=lambda: [janela_localiza_unidades.withdraw(), janela_principal()], hover_color='green', width=260, text_color='black')
    botao_voltar.place(relx=0, rely=1.0, anchor="sw")


def janela_historico_receitas():

    # Cria uma nova janela para localizar o historico de receitas do paciente
    janela_historico_receitas = ctk.CTkToplevel()
    janela_historico_receitas.config(bg='#161C25')
    janela_historico_receitas.geometry('900x700')
    janela_historico_receitas.resizable(False, False)
    janela_historico_receitas.title("Histórico do receituário médico")
    
    image_path = r".\midia/template.png"
    image = ctk.CTkImage(light_image= Image.open(image_path), size=(900,200))  # Redimensionar a imagem para o tamanho da janela
    image_label = ctk.CTkLabel(janela_historico_receitas, image=image, text="")
    image_label.place(x = 0, y =0)

    button_appearance_mode = ctk.CTkButton(master=janela_historico_receitas, text="Mudar Tema", command=change_appearance_mode, hover_color='green')
    button_appearance_mode.pack(pady=5, padx=5)
    button_appearance_mode.place(relx=1.0, rely=0, x=-5, y=5, anchor="ne")


    # Criar os elementos da interface
    font1 = ('Arial',20,'bold')
    font2 = ('Arial',12,'bold')

    id_label = ctk.CTkLabel(janela_historico_receitas, font=font1,text='ID:',text_color='#fff',bg_color='#161C25')
    id_label.place(x=20,y=260)

    id_entry = ctk.CTkEntry(janela_historico_receitas, font=font1,text_color='#000',fg_color='#fff', border_color='#0C9295', border_width=2, width=180)
    id_entry.place(x=100,y=260)

    nome_label = ctk.CTkLabel(janela_historico_receitas, font=font1,text='Nome:',text_color='#fff',bg_color='#161C25')
    nome_label.place(x=20,y=340)

    nome_entry = ctk.CTkEntry(janela_historico_receitas, font=font1,text_color='#000',fg_color='#fff', border_color='#0C9295', border_width=2, width=180)
    nome_entry.place(x=100,y=340)

    cargo_label = ctk.CTkLabel(janela_historico_receitas, font=font1,text='Cargo:',text_color='#fff',bg_color='#161C25')
    cargo_label.place(x=20,y=400)

    cargo_entry = ctk.CTkEntry(janela_historico_receitas, font=font1,text_color='#000',fg_color='#fff', border_color='#0C9295', border_width=2, width=180)
    cargo_entry.place(x=100,y=400)

    genero_label = ctk.CTkLabel(janela_historico_receitas, font=font1,text='Gênero:',text_color='#fff',bg_color='#161C25')
    genero_label.place(x=20,y=460)

    options = ['Feminino','Masculino']
    variable1 = str()

    genero_options = ctk.CTkComboBox(janela_historico_receitas, font=font1, text_color='#000',fg_color='#fff', dropdown_hover_color='#0C9295', button_color='#0C9295', button_hover_color='#0C9295',border_color='#0C9295',width=180,variable=variable1, values=options, state='readonly')
    genero_options.set('Male')
    genero_options.place(x=100,y=460)

    status_label = ctk.CTkLabel(janela_historico_receitas, font=font1,text='Status:',text_color='#fff',bg_color='#161C25')
    status_label.place(x=20,y=540)

    status_entry = ctk.CTkEntry(janela_historico_receitas, font=font1,text_color='#000',fg_color='#fff', border_color='#0C9295', border_width=2, width=180)
    status_entry.place(x=100,y=540)

    adicionar_botao = ctk.CTkButton(janela_historico_receitas,font=font1,text_color='#fff',text='Adicionar', fg_color='#05A312',hover_color='#00850B',bg_color='#161C25', cursor='hand2',corner_radius=15,width=260)
    adicionar_botao.place(x=20,y=590)

    limpar_botao = ctk.CTkButton(janela_historico_receitas,font=font1,text_color='#fff',text='Limpar', fg_color='#161C25',hover_color='#FF5002',bg_color='#161C25',border_color='#F15704',border_width=2,cursor='hand2',corner_radius=15,width=260)
    limpar_botao.place(x=20,y=630)

    atualizar_botao = ctk.CTkButton(janela_historico_receitas,font=font1,text_color='#fff',text='Atualizar', fg_color='#161C25',hover_color='#FF5002',bg_color='#161C25',border_color='#F15704',border_width=2,cursor='hand2',corner_radius=15,width=260)
    atualizar_botao.place(x=300,y=630)

    deletar_botao = ctk.CTkButton(janela_historico_receitas,font=font1,text_color='#fff',text='Deletar', fg_color='#E40404',hover_color='#AE0000',bg_color='#161C25',border_color='#E40404',border_width=2,cursor='hand2',corner_radius=15,width=260)
    deletar_botao.place(x=580,y=630)

    estilo = ttk.Style(janela_historico_receitas)
    estilo.theme_use('clam')
    estilo.configure('Treeview',font=font2,foreground='#fff',background='#000', fieldbackground='#313837')
    estilo.map('Treeview',background=[('selected', '#1A8F2D')])

    tree =ttk.Treeview(janela_historico_receitas,height=15)

    tree['columns'] = ('ID', 'Nome', 'Cargo', 'Genero', 'Status')

    tree.column('#0', width=0, stretch=tk.NO)
    tree.column('ID',anchor=tk.CENTER, width=100)
    tree.column('Nome',anchor=tk.CENTER, width=120)
    tree.column('Cargo',anchor=tk.CENTER, width=120)
    tree.column('Genero',anchor=tk.CENTER, width=120)
    tree.column('Status',anchor=tk.CENTER, width=120)

    tree.heading('ID', text='ID')
    tree.heading('Nome', text='Nome')
    tree.heading('Cargo', text='Cargo')
    tree.heading('Genero', text='Genero')
    tree.heading('Status', text='Status')

    tree.place(x=300,y=260)




    
    # Botão para enviar os dados
    botao_voltar = ctk.CTkButton(janela_historico_receitas, text="Voltar para página principal", command=lambda: [janela_historico_receitas.withdraw(), janela_principal()], hover_color='green', width=260, text_color='black')
    botao_voltar.place(relx=0, rely=1.0, anchor="sw")

def janela_cartao_paciente():

    # Cria uma nova janela para localizar as unidades médicas disponíveis
    janela_cartao_paciente = ctk.CTkToplevel()
    janela_cartao_paciente.config(bg='#161C25')
    janela_cartao_paciente.geometry('900x700')
    janela_cartao_paciente.resizable(False, False)
    janela_cartao_paciente.title("Cartão - Saúde Conectada")
    
    image_path = r".\midia/template.png"
    image = ctk.CTkImage(light_image= Image.open(image_path), size=(900,200))  # Redimensionar a imagem para o tamanho da janela
    image_label = ctk.CTkLabel(janela_cartao_paciente, image=image, text="")
    image_label.place(x = 0, y =0)

    button_appearance_mode = ctk.CTkButton(master=janela_cartao_paciente, text="Mudar Tema", command=change_appearance_mode, hover_color='green')
    button_appearance_mode.pack(pady=5, padx=5)
    button_appearance_mode.place(relx=1.0, rely=0, x=-5, y=5, anchor="ne")
    
    # Botão para enviar os dados
    botao_voltar = ctk.CTkButton(janela_cartao_paciente, text="Voltar para página principal", command=lambda: [janela_cartao_paciente.withdraw(), janela_principal()], hover_color='green', width=260, text_color='black')
    botao_voltar.place(relx=0, rely=1.0, anchor="sw")


def janela_medicamentos():

    # Cria uma nova janela para localizar os medicamentos disponíveis
    janela_medicamentos = ctk.CTkToplevel()
    janela_medicamentos.config(bg='#161C25')
    janela_medicamentos.geometry('900x700')
    janela_medicamentos.resizable(False, False)
    janela_medicamentos.title("Medicamentos disponíveis")
    
    image_path = r".\midia/template.png"
    image = ctk.CTkImage(light_image= Image.open(image_path), size=(900,200))  # Redimensionar a imagem para o tamanho da janela
    image_label = ctk.CTkLabel(janela_medicamentos, image=image, text="")
    image_label.place(x = 0, y =0)

    button_appearance_mode = ctk.CTkButton(master=janela_medicamentos, text="Mudar Tema", command=change_appearance_mode, hover_color='green')
    button_appearance_mode.pack(pady=5, padx=5)
    button_appearance_mode.place(relx=1.0, rely=0, x=-5, y=5, anchor="ne")


    # Criar os elementos da interface
    font1 = ('Arial',20,'bold')
    font2 = ('Arial',12,'bold')

    id_label = ctk.CTkLabel(janela_medicamentos, font=font1,text='ID:',text_color='#fff',bg_color='#161C25')
    id_label.place(x=20,y=260)

    id_entry = ctk.CTkEntry(janela_medicamentos, font=font1,text_color='#000',fg_color='#fff', border_color='#0C9295', border_width=2, width=180)
    id_entry.place(x=100,y=260)

    nome_label = ctk.CTkLabel(janela_medicamentos, font=font1,text='Nome:',text_color='#fff',bg_color='#161C25')
    nome_label.place(x=20,y=340)

    nome_entry = ctk.CTkEntry(janela_medicamentos, font=font1,text_color='#000',fg_color='#fff', border_color='#0C9295', border_width=2, width=180)
    nome_entry.place(x=100,y=340)

    cargo_label = ctk.CTkLabel(janela_medicamentos, font=font1,text='Cargo:',text_color='#fff',bg_color='#161C25')
    cargo_label.place(x=20,y=400)

    cargo_entry = ctk.CTkEntry(janela_medicamentos, font=font1,text_color='#000',fg_color='#fff', border_color='#0C9295', border_width=2, width=180)
    cargo_entry.place(x=100,y=400)

    genero_label = ctk.CTkLabel(janela_medicamentos, font=font1,text='Gênero:',text_color='#fff',bg_color='#161C25')
    genero_label.place(x=20,y=460)

    options = ['Feminino','Masculino']
    variable1 = str()

    genero_options = ctk.CTkComboBox(janela_medicamentos, font=font1, text_color='#000',fg_color='#fff', dropdown_hover_color='#0C9295', button_color='#0C9295', button_hover_color='#0C9295',border_color='#0C9295',width=180,variable=variable1, values=options, state='readonly')
    genero_options.set('Male')
    genero_options.place(x=100,y=460)

    status_label = ctk.CTkLabel(janela_medicamentos, font=font1,text='Status:',text_color='#fff',bg_color='#161C25')
    status_label.place(x=20,y=540)

    status_entry = ctk.CTkEntry(janela_medicamentos, font=font1,text_color='#000',fg_color='#fff', border_color='#0C9295', border_width=2, width=180)
    status_entry.place(x=100,y=540)

    adicionar_botao = ctk.CTkButton(janela_medicamentos,font=font1,text_color='#fff',text='Adicionar', fg_color='#05A312',hover_color='#00850B',bg_color='#161C25', cursor='hand2',corner_radius=15,width=260)
    adicionar_botao.place(x=20,y=590)

    limpar_botao = ctk.CTkButton(janela_medicamentos,font=font1,text_color='#fff',text='Limpar', fg_color='#161C25',hover_color='#FF5002',bg_color='#161C25',border_color='#F15704',border_width=2,cursor='hand2',corner_radius=15,width=260)
    limpar_botao.place(x=20,y=630)

    atualizar_botao = ctk.CTkButton(janela_medicamentos,font=font1,text_color='#fff',text='Atualizar', fg_color='#161C25',hover_color='#FF5002',bg_color='#161C25',border_color='#F15704',border_width=2,cursor='hand2',corner_radius=15,width=260)
    atualizar_botao.place(x=300,y=630)

    deletar_botao = ctk.CTkButton(janela_medicamentos,font=font1,text_color='#fff',text='Deletar', fg_color='#E40404',hover_color='#AE0000',bg_color='#161C25',border_color='#E40404',border_width=2,cursor='hand2',corner_radius=15,width=260)
    deletar_botao.place(x=580,y=630)

    estilo = ttk.Style(janela_medicamentos)
    estilo.theme_use('clam')
    estilo.configure('Treeview',font=font2,foreground='#fff',background='#000', fieldbackground='#313837')
    estilo.map('Treeview',background=[('selected', '#1A8F2D')])

    tree =ttk.Treeview(janela_medicamentos,height=15)

    tree['columns'] = ('ID', 'Nome', 'Cargo', 'Genero', 'Status')

    tree.column('#0', width=0, stretch=tk.NO)
    tree.column('ID',anchor=tk.CENTER, width=100)
    tree.column('Nome',anchor=tk.CENTER, width=120)
    tree.column('Cargo',anchor=tk.CENTER, width=120)
    tree.column('Genero',anchor=tk.CENTER, width=120)
    tree.column('Status',anchor=tk.CENTER, width=120)

    tree.heading('ID', text='ID')
    tree.heading('Nome', text='Nome')
    tree.heading('Cargo', text='Cargo')
    tree.heading('Genero', text='Genero')
    tree.heading('Status', text='Status')

    tree.place(x=300,y=260)



    
    # Botão para enviar os dados
    botao_voltar = ctk.CTkButton(janela_medicamentos, text="Voltar para página principal", command=lambda: [janela_medicamentos.withdraw(), janela_principal()], hover_color='green', width=260, text_color='black')
    botao_voltar.place(relx=0, rely=1.0, anchor="sw")

def janela_ouvidoria():

    # Cria uma nova janela para localizar a ouvidoria
    janela_ouvidoria = ctk.CTkToplevel(fg_color='#03dffc')
    janela_ouvidoria.geometry('900x700')
    janela_ouvidoria.resizable(False, False)
    janela_ouvidoria.title("Ouvidoria")
    
    image_path = r".\midia/template.png"
    image = ctk.CTkImage(light_image= Image.open(image_path), size=(900,200))  # Redimensionar a imagem para o tamanho da janela
    image_label = ctk.CTkLabel(janela_ouvidoria, image=image, text="")
    image_label.place(x = 0, y =0)

    button_appearance_mode = ctk.CTkButton(master=janela_ouvidoria, text="Mudar Tema", command=change_appearance_mode, hover_color='green')
    button_appearance_mode.pack(pady=5, padx=5)
    button_appearance_mode.place(relx=1.0, rely=0, x=-5, y=5, anchor="ne")
    
    # Cria os rótulos
    label_titulo = ctk.CTkLabel(janela_ouvidoria, text="Ouvidoria", font=("Arial", 44), text_color='yellow')
    label_numero = ctk.CTkLabel(janela_ouvidoria, text="Número da Ouvidoria: 0800 123 4567", font=("Arial", 24), text_color='yellow')
    label_informacoes = ctk.CTkLabel(janela_ouvidoria, text="Para outras informações, acesse nosso site.", font=("Arial", 24), text_color='yellow')

    # Posiciona os rótulos
    label_titulo.place(x=300, y=250)
    label_numero.place(x=215, y=350)
    label_informacoes.place(x=190, y=450)
    
    # Botão para enviar os dados
    botao_voltar = ctk.CTkButton(janela_ouvidoria, text="Voltar para página principal", command=lambda: [janela_ouvidoria.withdraw(), janela_principal()], hover_color='green', width=260, text_color='black')
    botao_voltar.place(relx=0, rely=1.0, anchor="sw")

