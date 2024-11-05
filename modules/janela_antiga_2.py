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
    janela.geometry('1450x1017')
    janela.resizable(False, False)
    return janela



def change_appearance_mode():
    global appearance_mode
    appearance_mode = "dark" if appearance_mode == "light" else "light"
    ctk.set_appearance_mode(appearance_mode)

def janela_criar_conta():

    # Cria uma nova janela para o cadastro
    janela_cadastro = ctk.CTkToplevel(fg_color='#03dffc')
    janela_cadastro.geometry('1450x1017')
    janela_cadastro.resizable(False, False)
    janela_cadastro.title("Criar Conta")

    image_path = r".\midia/template.png"
    image = ctk.CTkImage(light_image= Image.open(image_path), size=(1450,300))  # Redimensionar a imagem para o tamanho da janela
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
            label_mensagem.place(x=580, y=890)
            # Após 2 segundos, remove a label da tela
            janela_cadastro.after(2000, label_mensagem.destroy)
            #janela_cadastro.withdraw()
        
        elif verifica_email == False or valida_senha == False or data_nascimento == False or telefone == False or cpf == False:

            # Exibir uma mensagem de erro se algum campo estiver fora do padrão necessário
            print('Algum campo está fora do padrão necessário')
            label_mensagem = ctk.CTkLabel(janela_cadastro, text="Erro!! Por favor, preencha todos os campos no formato correto", font=("Arial", 12), bg_color='#fc031c', text_color='black')
            label_mensagem.place(x=550, y=890)
            # Após 2 segundos, remove a label da tela
            janela_cadastro.after(2000, label_mensagem.destroy)
            #janela_cadastro.withdraw()
            
        else:
            # Botão para enviar os dados
            print(f"Nome: {nome}, Email: {email}, CPF: {cpf}, Telefone: {telefone}, Dt_nascimento: {data_nascimento}, Senha: {senha}")  # Exemplo simples de impressão
            
            # Verifica se o cpf ja existe
            verifica_cadastro = db.verifica_cadastro(cpf)
            print(f'verifica :{verifica_cadastro}')
            if not verifica_cadastro.empty:
                # Exibir uma mensagem de erro se algum campo estiver fora do padrão necessário
                print('cpf ja cadastrado!')
                label_mensagem = ctk.CTkLabel(janela_cadastro, text="Erro!! CPF já cadastrado!", font=("Arial", 12), bg_color='#fc031c', text_color='black')
                label_mensagem.place(x=630, y=860)
                # Após 2 segundos, remove a label da tela
                janela_cadastro.after(2000, label_mensagem.destroy)
                #janela_cadastro.withdraw()

            else:
                db.cadastro_usuario(nome,email,senha,data_nascimento,telefone,cpf)
                label_mensagem = ctk.CTkLabel(janela_cadastro, text="Cadastro realizado com sucesso!!", font=("Arial", 12), bg_color='#61eb34', text_color='black')
                label_mensagem.place(x=580, y=890)
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
    botao_cadastrar.place(x=630, y=820)
    nome_label.place(x=400, y=410)
    nome_entry.place(x=400, y=450)
    email_label.place(x=400, y=560)
    email_entry.place(x=400, y=590)
    cpf_label.place(x=400, y=700)
    cpf_entry.place(x=400, y=730)
    telefone_label.place(x=850, y=410)
    telefone_entry.place(x=850, y=450)
    data_nascimento_label.place(x=850, y=560)
    data_nascimento_entry.place(x=850, y=590)
    senha_label.place(x=850, y=700)
    senha_entry.place(x=850, y=730)
    senha_requisitos.place(x=850, y=770)
    senha_requisitos1.place(x=850, y=790)
    senha_requisitos2.place(x=850, y=810)
    senha_requisitos3.place(x=850, y=830)
    senha_requisitos4.place(x=850, y=850)


def login(janela, cpf_valor, senha_valor):
    cpf_valor = '858.816.885-51'
    senha_valor = 'Gabigol123.'
    if cpf_valor == '' or senha_valor == '':
        # Exibir uma mensagem de erro se algum campo estiver vazio
        label_mensagem = ctk.CTkLabel(janela, text="Erro!!! Por favor, preencha todos os campos.", font=("Arial", 12), bg_color='#fc031c', text_color='black')
        label_mensagem.place(x = 50, y = 600)
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
            janela_principal(cpf_valor)
        else:
            # Exibir uma mensagem de erro se login ou senha nao for encontrado
            label_mensagem = ctk.CTkLabel(janela, text="Erro!!! Login ou senha inválidos.", font=("Arial", 12), bg_color='#fc031c', text_color='black')
            label_mensagem.place(x = 50, y = 600)
            # Após 2 segundos, remove a label da tela
            janela.after(4000, label_mensagem.destroy)

        

def janela_login(cpf_valor):

    # Carregar a imagem
    janela = ctk.CTkToplevel(fg_color='#03dffc')
    janela.geometry('1450x1017')
    janela.resizable(False, False)

    janela.title("Tela de Login")
    image_path = r".\midia/login.png"

    image = ctk.CTkImage(light_image= Image.open(image_path), size=(1450,1017))  # Redimensionar a imagem para o tamanho da janela
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
    texto.place(x = 85, y = 300)

    cpf = ctk.CTkEntry(janela, placeholder_text='CPF (___.___.___-__)')
    cpf.place(x = 50, y = 350)

    senha = ctk.CTkEntry(janela, placeholder_text='Sua senha', show='*')
    senha.place(x = 50, y = 400)

    checkbox = ctk.CTkCheckBox(janela, text='Lembrar Login', bg_color='#03dffc', text_color='black')
    checkbox.place(x = 50, y = 450)

    # Botão para criar conta na tela principal
    botao_criar_conta = ctk.CTkButton(janela, text="Criar Conta", command=lambda: [janela_criar_conta(), janela.withdraw()], hover_color='green')
    botao_criar_conta.place(x = 50, y = 500)
    

    botao = ctk.CTkButton(janela, text='Login', command=login_click, hover_color='green')
    botao.place(x = 50, y = 550)
    janela.mainloop()


def janela_principal(cpf_valor):

    # Cria uma nova janela para o cadastro
    janela_principal = ctk.CTkToplevel(fg_color='#03dffc')
    janela_principal.geometry('1450x1017')
    janela_principal.resizable(False, False)
    janela_principal.title("Saúde conectada")
    
    image_path = r".\midia/template.png"
    image = ctk.CTkImage(light_image= Image.open(image_path), size=(1450,300))  # Redimensionar a imagem para o tamanho da janela
    image_label = ctk.CTkLabel(janela_principal, image=image, text="")
    image_label.place(x = 0, y =0)

    button_appearance_mode = ctk.CTkButton(master=janela_principal, text="Mudar Tema", command=change_appearance_mode, hover_color='green')
    button_appearance_mode.pack(pady=5, padx=5)
    button_appearance_mode.place(relx=1.0, rely=0, x=-5, y=5, anchor="ne")
    
    # Botões
    image_path = r".\midia/saúde.png"
    image = ctk.CTkImage(light_image= Image.open(image_path), size=(150,150))  # Redimensionar a imagem para o tamanho da janela
    image_label = ctk.CTkButton(janela_principal, image=image, text='Acompanhe seu histórico de atendimentos', command=lambda: [janela_principal.withdraw(), janela_historico_atendimentos(cpf_valor)], compound='top', fg_color='#03dffc', text_color='black', width=260)
    image_label.place(x = 350, y =300)

    image_path = r".\midia/hospital.png"
    image = ctk.CTkImage(light_image= Image.open(image_path), size=(150,150))  # Redimensionar a imagem para o tamanho da janela
    image_label = ctk.CTkButton(janela_principal, image=image, text='Localize as unidades disponíveis', command=lambda: [janela_principal.withdraw(), janela_localiza_unidades(cpf_valor)], compound='top', fg_color='#03dffc', text_color='black', width=260)
    image_label.place(x=350, y=530)

    image_path = r".\midia/receita.png"
    image = ctk.CTkImage(light_image= Image.open(image_path), size=(150,150))  # Redimensionar a imagem para o tamanho da janela
    image_label = ctk.CTkButton(janela_principal, image=image, text='Verifique suas ultimas receitas aqui', command=lambda: [janela_principal.withdraw(), janela_historico_receitas(cpf_valor)], compound='top', fg_color='#03dffc', text_color='black', width=260)
    image_label.place(x=350, y=780)

    image_path = r".\midia/cartao.png"
    image = ctk.CTkImage(light_image= Image.open(image_path), size=(150,150))  # Redimensionar a imagem para o tamanho da janela
    image_label = ctk.CTkButton(janela_principal, image=image, text='Acessar cartão', command=lambda: [janela_principal.withdraw(), janela_cartao_paciente(cpf_valor)], compound='top', fg_color='#03dffc', text_color='black', width=260)
    image_label.place(x=750, y=300)

    image_path = r".\midia/medicamento.png"
    image = ctk.CTkImage(light_image= Image.open(image_path), size=(150,150))  # Redimensionar a imagem para o tamanho da janela
    image_label = ctk.CTkButton(janela_principal, image=image, text='Disponibilidade medicamentos', command=lambda: [janela_principal.withdraw(), janela_medicamentos(cpf_valor)], compound='top', fg_color='#03dffc', text_color='black', width=260)
    image_label.place(x=750, y=530)

    image_path = r".\midia/ouvidoria.png"
    image = ctk.CTkImage(light_image= Image.open(image_path), size=(150,150))  # Redimensionar a imagem para o tamanho da janela
    image_label = ctk.CTkButton(janela_principal, image=image, text='Ouvidoria - Saúde conectada', command=lambda: [janela_principal.withdraw(), janela_ouvidoria(cpf_valor)], compound='top', fg_color='#03dffc', text_color='black', width=260)
    image_label.place(x=750, y=780)


    # Botão para enviar os dados
    botao_voltar = ctk.CTkButton(janela_principal, text="Voltar para página de login", command=lambda: [janela_principal.withdraw(), janela_login(cpf_valor)], hover_color='green', width=260, text_color='black')
    botao_voltar.place(relx=0, rely=1.0, anchor="sw")

def janela_historico_atendimentos(cpf_valor):

    # Cria uma nova janela para o histórico de atendimentos do paciente
    janela_historico_atendimentos = ctk.CTkToplevel()
    janela_historico_atendimentos.config(bg='#161C25')
    janela_historico_atendimentos.geometry('1450x1017')
    janela_historico_atendimentos.resizable(False, False)
    janela_historico_atendimentos.title("Histórico de atendimentos")
    
    image_path = r".\midia/template.png"
    image = ctk.CTkImage(light_image= Image.open(image_path), size=(1450,300))  # Redimensionar a imagem para o tamanho da janela
    image_label = ctk.CTkLabel(janela_historico_atendimentos, image=image, text="")
    image_label.place(x = 0, y =0)

    button_appearance_mode = ctk.CTkButton(master=janela_historico_atendimentos, text="Mudar Tema", command=change_appearance_mode, hover_color='green')
    button_appearance_mode.pack(pady=5, padx=5)
    button_appearance_mode.place(relx=1.0, rely=0, x=-5, y=5, anchor="ne")

    # Criar os elementos da interface
    font1 = ('Arial',20,'bold')
    font2 = ('Arial',12,'bold')
    font3 = ('Arial',17,'bold')

    nome_label = ctk.CTkLabel(janela_historico_atendimentos, font=font3,text='Paciente:',text_color='#fff',bg_color='#161C25')
    nome_label.place(x=20,y=320)

    nome_entry = ctk.CTkEntry(janela_historico_atendimentos, font=font1,text_color='#000',fg_color='#fff', border_color='#0C9295', border_width=2, width=180)
    nome_entry.place(x=100,y=320)

    options_especialidade = ['Cardiologista','Cirurgião Geral','Dermatologista','Podólogo']
    variable_especialidade = str()

    especialidade_label = ctk.CTkLabel(janela_historico_atendimentos, font=font3,text='Especi\nalidade:',text_color='#fff',bg_color='#161C25')
    especialidade_label.place(x=20,y=400)

    especialidade_options = ctk.CTkComboBox(janela_historico_atendimentos, font=font2, text_color='#000',fg_color='#fff', dropdown_hover_color='#0C9295', button_color='#0C9295', button_hover_color='#0C9295',border_color='#0C9295',width=180,variable=variable_especialidade, values=options_especialidade, state='readonly')
    especialidade_options.set('')
    especialidade_options.place(x=100,y=400)

    plano_saude_label = ctk.CTkLabel(janela_historico_atendimentos, font=font3,text='Plano de\nsaúde:',text_color='#fff',bg_color='#161C25')
    plano_saude_label.place(x=20,y=480)

    plano_saude_entry = ctk.CTkEntry(janela_historico_atendimentos, font=font1,text_color='#000',fg_color='#fff', border_color='#0C9295', border_width=2, width=180)
    plano_saude_entry.place(x=100,y=480)

    options_plano_saude = ['Amil','Bradesco','SulAmérica','Hapvida','Planserv','Intermédica']
    variable_plano_saude = str()

    plano_saude_options = ctk.CTkComboBox(janela_historico_atendimentos, font=font1, text_color='#000',fg_color='#fff', dropdown_hover_color='#0C9295', button_color='#0C9295', button_hover_color='#0C9295',border_color='#0C9295',width=180,variable=variable_plano_saude, values=options_plano_saude, state='readonly')
    plano_saude_options.set('')
    plano_saude_options.place(x=100,y=480)

    data_consulta_label = ctk.CTkLabel(janela_historico_atendimentos, font=font3,text='Data da\nConsulta:',text_color='#fff',bg_color='#161C25')
    data_consulta_label.place(x=20,y=560)

    data_consulta_entry = ctk.CTkEntry(janela_historico_atendimentos, font=font1,text_color='#000',fg_color='#fff', border_color='#0C9295', border_width=2, width=180)
    data_consulta_entry.place(x=100,y=560)

    horario_label = ctk.CTkLabel(janela_historico_atendimentos, font=font1,text='Horário:',text_color='#fff',bg_color='#161C25')
    horario_label.place(x=20,y=640)

    options_horario = ['08:00:00','09:00:00','10:00:00','11:00:00','13:00:00','14:00:00','15:00:00','16:00:00','17:00:00']
    variable_horario = str()

    horario_options = ctk.CTkComboBox(janela_historico_atendimentos, font=font1, text_color='#000',fg_color='#fff', dropdown_hover_color='#0C9295', button_color='#0C9295', button_hover_color='#0C9295',border_color='#0C9295',width=180,variable=variable_horario, values=options_horario, state='readonly')
    horario_options.set('')
    horario_options.place(x=100,y=640)

    status_label = ctk.CTkLabel(janela_historico_atendimentos, font=font1,text='Status:',text_color='#fff',bg_color='#161C25')
    status_label.place(x=20,y=730)

    options = ['Cancelado','Realizado','Pendente']
    variable1 = str()

    status_options = ctk.CTkComboBox(janela_historico_atendimentos, font=font1, text_color='#000',fg_color='#fff', dropdown_hover_color='#0C9295', button_color='#0C9295', button_hover_color='#0C9295',border_color='#0C9295',width=180,variable=variable1, values=options, state='readonly')
    status_options.set('')
    status_options.place(x=100,y=730)

    medico_label = ctk.CTkLabel(janela_historico_atendimentos, font=font1,text='Médico:',text_color='#fff',bg_color='#161C25')
    medico_label.place(x=20,y=840)

    options_medico = ['Jurandir Rosa','Natã Silva','Riquelme Queiroz','Roberto Passos']
    variable_medico = str()

    medico_options = ctk.CTkComboBox(janela_historico_atendimentos, font=font1, text_color='#000',fg_color='#fff', dropdown_hover_color='#0C9295', button_color='#0C9295', button_hover_color='#0C9295',border_color='#0C9295',width=180,variable=variable_medico, values=options_medico, state='readonly')
    medico_options.set('')
    medico_options.place(x=100,y=840)

    adicionar_botao = ctk.CTkButton(janela_historico_atendimentos,font=font1,text_color='#fff',text='Adicionar', command=lambda: [db.adicionar_atendimentos(tree, nome_entry.get(), medico_options.get(), data_consulta_entry.get(), horario_options.get(), plano_saude_options.get(), status_options.get(), especialidade_options.get(), cpf_valor)], fg_color='#05A312',hover_color='#00850B',bg_color='#161C25', cursor='hand2',corner_radius=15,width=260)
    adicionar_botao.place(x=300,y=900)
    
    pesquisar_botao = ctk.CTkButton(janela_historico_atendimentos,font=font1,text_color='#fff',text='Pesquisar', command=lambda: [db.pesquisar_atendimentos(tree, nome_entry.get(), medico_options.get(), data_consulta_entry.get(), horario_options.get(), plano_saude_options.get(), status_options.get(), especialidade_options.get(), cpf_valor)], fg_color='#161C25',hover_color='#FF5002',bg_color='#161C25',border_color='#F15704',border_width=2,cursor='hand2',corner_radius=15,width=260)
    pesquisar_botao.place(x=20,y=900)

    atualizar_botao = ctk.CTkButton(janela_historico_atendimentos,font=font1,text_color='#fff',text='Atualizar', command=lambda: [db.update_atendimentos(tree, medico_options.get(), plano_saude_options.get(), status_options.get(), data_consulta_entry.get(), horario_options.get())], fg_color='#161C25',hover_color='#FF5002',bg_color='#161C25',border_color='#F15704',border_width=2,cursor='hand2',corner_radius=15,width=260)
    atualizar_botao.place(x=580,y=900)
    
    deletar_botao = ctk.CTkButton(janela_historico_atendimentos,font=font1,text_color='#fff',text='Deletar', command=lambda: [db.deletar_atendimentos(tree, cpf_valor)], fg_color='#E40404',hover_color='#AE0000',bg_color='#161C25',border_color='#E40404',border_width=2,cursor='hand2',corner_radius=15,width=260)
    deletar_botao.place(x=860,y=900)

    limpar_botao = ctk.CTkButton(janela_historico_atendimentos,font=font1,text_color='#fff',text='Limpar', command=lambda: [db.limpar_campo(tree)], fg_color='#161C25',hover_color='#AE0000',bg_color='#161C25',border_color='#E40404',border_width=2,cursor='hand2',corner_radius=15,width=260)
    limpar_botao.place(x=1140,y=900)

    estilo = ttk.Style(janela_historico_atendimentos)
    estilo.theme_use('clam')
    estilo.configure('Treeview',font=font2,foreground='#fff',background='#000', fieldbackground='#313837')
    estilo.map('Treeview',background=[('selected', '#1A8F2D')])

    tree =ttk.Treeview(janela_historico_atendimentos,height=25)

    tree['columns'] = ( 'Paciente', 'Médico', 'Plano', 'Data da consulta', 'Horário', 'Especialidade', 'Status')

    tree.column('#0', width=0, stretch=tk.NO)
    tree.column('Paciente',anchor=tk.CENTER, width=165)
    tree.column('Médico',anchor=tk.CENTER, width=165)
    tree.column('Plano',anchor=tk.CENTER, width=180)
    tree.column('Data da consulta',anchor=tk.CENTER, width=110)
    tree.column('Horário',anchor=tk.CENTER, width=110)
    tree.column('Especialidade',anchor=tk.CENTER, width=180)
    tree.column('Status',anchor=tk.CENTER, width=170)

    tree.heading('Paciente', text='Paciente')
    tree.heading('Médico', text='Médico')
    tree.heading('Plano', text='Plano')
    tree.heading('Data da consulta', text='Data da consulta')
    tree.heading('Horário', text='Horário')
    tree.heading('Especialidade', text='Especialidade')
    tree.heading('Status', text='Status')

    tree.place(x=350,y=320)


    # Botão para enviar os dados
    botao_voltar = ctk.CTkButton(janela_historico_atendimentos, text="Voltar para página principal", command=lambda: [janela_historico_atendimentos.withdraw(), janela_principal(cpf_valor)], hover_color='green', width=260, text_color='black')
    botao_voltar.place(relx=0, rely=1.0, anchor="sw")


def janela_localiza_unidades(cpf_valor):

    # Cria uma nova janela para localizar as unidades médicas disponíveis
    janela_localiza_unidades = ctk.CTkToplevel()
    janela_localiza_unidades.config(bg='#161C25')
    janela_localiza_unidades.geometry('1450x1017')
    janela_localiza_unidades.resizable(False, False)
    janela_localiza_unidades.title("Unidades médicas")
    
    image_path = r".\midia/template.png"
    image = ctk.CTkImage(light_image= Image.open(image_path), size=(1450,300))  # Redimensionar a imagem para o tamanho da janela
    image_label = ctk.CTkLabel(janela_localiza_unidades, image=image, text="")
    image_label.place(x = 0, y =0)

    button_appearance_mode = ctk.CTkButton(master=janela_localiza_unidades, text="Mudar Tema", command=change_appearance_mode, hover_color='green')
    button_appearance_mode.pack(pady=5, padx=5)
    button_appearance_mode.place(relx=1.0, rely=0, x=-5, y=5, anchor="ne")

    # Criar os elementos da interface
    font1 = ('Arial',20,'bold')
    font2 = ('Arial',12,'bold')

    id_label = ctk.CTkLabel(janela_localiza_unidades, font=font1,text='ID:',text_color='#fff',bg_color='#161C25')
    id_label.place(x=20,y=400)

    id_entry = ctk.CTkEntry(janela_localiza_unidades, font=font1,text_color='#000',fg_color='#fff', border_color='#0C9295', border_width=2, width=180)
    id_entry.place(x=100,y=400)

    nome_label = ctk.CTkLabel(janela_localiza_unidades, font=font1,text='Nome:',text_color='#fff',bg_color='#161C25')
    nome_label.place(x=20,y=480)

    nome_entry = ctk.CTkEntry(janela_localiza_unidades, font=font1,text_color='#000',fg_color='#fff', border_color='#0C9295', border_width=2, width=180)
    nome_entry.place(x=100,y=480)

    cargo_label = ctk.CTkLabel(janela_localiza_unidades, font=font1,text='Cargo:',text_color='#fff',bg_color='#161C25')
    cargo_label.place(x=20,y=560)

    cargo_entry = ctk.CTkEntry(janela_localiza_unidades, font=font1,text_color='#000',fg_color='#fff', border_color='#0C9295', border_width=2, width=180)
    cargo_entry.place(x=100,y=560)

    genero_label = ctk.CTkLabel(janela_localiza_unidades, font=font1,text='Gênero:',text_color='#fff',bg_color='#161C25')
    genero_label.place(x=20,y=640)

    options = ['Feminino','Masculino']
    variable1 = str()

    genero_options = ctk.CTkComboBox(janela_localiza_unidades, font=font1, text_color='#000',fg_color='#fff', dropdown_hover_color='#0C9295', button_color='#0C9295', button_hover_color='#0C9295',border_color='#0C9295',width=180,variable=variable1, values=options, state='readonly')
    genero_options.set('Male')
    genero_options.place(x=100,y=640)

    status_label = ctk.CTkLabel(janela_localiza_unidades, font=font1,text='Status:',text_color='#fff',bg_color='#161C25')
    status_label.place(x=20,y=730)

    status_entry = ctk.CTkEntry(janela_localiza_unidades, font=font1,text_color='#000',fg_color='#fff', border_color='#0C9295', border_width=2, width=180)
    status_entry.place(x=100,y=730)

    adicionar_botao = ctk.CTkButton(janela_localiza_unidades,font=font1,text_color='#fff',text='Adicionar', fg_color='#05A312',hover_color='#00850B',bg_color='#161C25', cursor='hand2',corner_radius=15,width=260)
    adicionar_botao.place(x=20,y=830)

    limpar_botao = ctk.CTkButton(janela_localiza_unidades,font=font1,text_color='#fff',text='Limpar', fg_color='#161C25',hover_color='#FF5002',bg_color='#161C25',border_color='#F15704',border_width=2,cursor='hand2',corner_radius=15,width=260)
    limpar_botao.place(x=20,y=880)

    atualizar_botao = ctk.CTkButton(janela_localiza_unidades,font=font1,text_color='#fff',text='Atualizar', fg_color='#161C25',hover_color='#FF5002',bg_color='#161C25',border_color='#F15704',border_width=2,cursor='hand2',corner_radius=15,width=260)
    atualizar_botao.place(x=300,y=880)

    deletar_botao = ctk.CTkButton(janela_localiza_unidades,font=font1,text_color='#fff',text='Deletar', fg_color='#E40404',hover_color='#AE0000',bg_color='#161C25',border_color='#E40404',border_width=2,cursor='hand2',corner_radius=15,width=260)
    deletar_botao.place(x=580,y=880)

    estilo = ttk.Style(janela_localiza_unidades)
    estilo.theme_use('clam')
    estilo.configure('Treeview',font=font2,foreground='#fff',background='#000', fieldbackground='#313837')
    estilo.map('Treeview',background=[('selected', '#1A8F2D')])

    tree =ttk.Treeview(janela_localiza_unidades,height=25)

    tree['columns'] = ('ID', 'Nome', 'Cargo', 'Genero', 'Status')

    tree.column('#0', width=0, stretch=tk.NO)
    tree.column('ID',anchor=tk.CENTER, width=200)
    tree.column('Nome',anchor=tk.CENTER, width=220)
    tree.column('Cargo',anchor=tk.CENTER, width=220)
    tree.column('Genero',anchor=tk.CENTER, width=220)
    tree.column('Status',anchor=tk.CENTER, width=220)

    tree.heading('ID', text='ID')
    tree.heading('Nome', text='Nome')
    tree.heading('Cargo', text='Cargo')
    tree.heading('Genero', text='Genero')
    tree.heading('Status', text='Status')

    tree.place(x=350,y=320)

    
    # Botão para enviar os dados
    botao_voltar = ctk.CTkButton(janela_localiza_unidades, text="Voltar para página principal", command=lambda: [janela_localiza_unidades.withdraw(), janela_principal(cpf_valor)], hover_color='green', width=260, text_color='black')
    botao_voltar.place(relx=0, rely=1.0, anchor="sw")


def janela_historico_receitas(cpf_valor):

    # Cria uma nova janela para localizar o historico de receitas do paciente
    janela_historico_receitas = ctk.CTkToplevel()
    janela_historico_receitas.config(bg='#161C25')
    janela_historico_receitas.geometry('1450x1017')
    janela_historico_receitas.resizable(False, False)
    janela_historico_receitas.title("Histórico do receituário médico")
    
    image_path = r".\midia/template.png"
    image = ctk.CTkImage(light_image= Image.open(image_path), size=(1450,300))  # Redimensionar a imagem para o tamanho da janela
    image_label = ctk.CTkLabel(janela_historico_receitas, image=image, text="")
    image_label.place(x = 0, y =0)

    button_appearance_mode = ctk.CTkButton(master=janela_historico_receitas, text="Mudar Tema", command=change_appearance_mode, hover_color='green')
    button_appearance_mode.pack(pady=5, padx=5)
    button_appearance_mode.place(relx=1.0, rely=0, x=-5, y=5, anchor="ne")


    # Criar os elementos da interface
    font1 = ('Arial',20,'bold')
    font2 = ('Arial',12,'bold')

    id_label = ctk.CTkLabel(janela_historico_receitas, font=font1,text='ID:',text_color='#fff',bg_color='#161C25')
    id_label.place(x=20,y=400)

    id_entry = ctk.CTkEntry(janela_historico_receitas, font=font1,text_color='#000',fg_color='#fff', border_color='#0C9295', border_width=2, width=180)
    id_entry.place(x=100,y=400)

    nome_label = ctk.CTkLabel(janela_historico_receitas, font=font1,text='Nome:',text_color='#fff',bg_color='#161C25')
    nome_label.place(x=20,y=480)

    nome_entry = ctk.CTkEntry(janela_historico_receitas, font=font1,text_color='#000',fg_color='#fff', border_color='#0C9295', border_width=2, width=180)
    nome_entry.place(x=100,y=480)

    cargo_label = ctk.CTkLabel(janela_historico_receitas, font=font1,text='Cargo:',text_color='#fff',bg_color='#161C25')
    cargo_label.place(x=20,y=560)

    cargo_entry = ctk.CTkEntry(janela_historico_receitas, font=font1,text_color='#000',fg_color='#fff', border_color='#0C9295', border_width=2, width=180)
    cargo_entry.place(x=100,y=560)

    genero_label = ctk.CTkLabel(janela_historico_receitas, font=font1,text='Gênero:',text_color='#fff',bg_color='#161C25')
    genero_label.place(x=20,y=640)

    options = ['Feminino','Masculino']
    variable1 = str()

    genero_options = ctk.CTkComboBox(janela_historico_receitas, font=font1, text_color='#000',fg_color='#fff', dropdown_hover_color='#0C9295', button_color='#0C9295', button_hover_color='#0C9295',border_color='#0C9295',width=180,variable=variable1, values=options, state='readonly')
    genero_options.set('Male')
    genero_options.place(x=100,y=640)

    status_label = ctk.CTkLabel(janela_historico_receitas, font=font1,text='Status:',text_color='#fff',bg_color='#161C25')
    status_label.place(x=20,y=730)

    status_entry = ctk.CTkEntry(janela_historico_receitas, font=font1,text_color='#000',fg_color='#fff', border_color='#0C9295', border_width=2, width=180)
    status_entry.place(x=100,y=730)

    adicionar_botao = ctk.CTkButton(janela_historico_receitas,font=font1,text_color='#fff',text='Adicionar', fg_color='#05A312',hover_color='#00850B',bg_color='#161C25', cursor='hand2',corner_radius=15,width=260)
    adicionar_botao.place(x=20,y=830)

    pesquisar_botao = ctk.CTkButton(janela_historico_receitas,font=font1,text_color='#fff',text='Pesquisar', command=lambda: [db.pesquisar_receitas(tree)], fg_color='#161C25',hover_color='#FF5002',bg_color='#161C25',border_color='#F15704',border_width=2,cursor='hand2',corner_radius=15,width=260)
    pesquisar_botao.place(x=20,y=880)

    atualizar_botao = ctk.CTkButton(janela_historico_receitas,font=font1,text_color='#fff',text='Atualizar', fg_color='#161C25',hover_color='#FF5002',bg_color='#161C25',border_color='#F15704',border_width=2,cursor='hand2',corner_radius=15,width=260)
    atualizar_botao.place(x=300,y=880)

    deletar_botao = ctk.CTkButton(janela_historico_receitas,font=font1,text_color='#fff',text='Deletar', fg_color='#E40404',hover_color='#AE0000',bg_color='#161C25',border_color='#E40404',border_width=2,cursor='hand2',corner_radius=15,width=260)
    deletar_botao.place(x=580,y=880)

    estilo = ttk.Style(janela_historico_receitas)
    estilo.theme_use('clam')
    estilo.configure('Treeview',font=font2,foreground='#fff',background='#000', fieldbackground='#313837')
    estilo.map('Treeview',background=[('selected', '#1A8F2D')])

    tree =ttk.Treeview(janela_historico_receitas,height=25)

    tree['columns'] = ('ID', 'Nome', 'Cargo', 'Genero', 'Status')

    tree.column('#0', width=0, stretch=tk.NO)
    tree.column('ID',anchor=tk.CENTER, width=200)
    tree.column('Nome',anchor=tk.CENTER, width=220)
    tree.column('Cargo',anchor=tk.CENTER, width=220)
    tree.column('Genero',anchor=tk.CENTER, width=220)
    tree.column('Status',anchor=tk.CENTER, width=220)

    tree.heading('ID', text='ID')
    tree.heading('Nome', text='Nome')
    tree.heading('Cargo', text='Cargo')
    tree.heading('Genero', text='Genero')
    tree.heading('Status', text='Status')

    tree.place(x=350,y=320)



    
    # Botão para enviar os dados
    botao_voltar = ctk.CTkButton(janela_historico_receitas, text="Voltar para página principal", command=lambda: [janela_historico_receitas.withdraw(), janela_principal(cpf_valor)], hover_color='green', width=260, text_color='black')
    botao_voltar.place(relx=0, rely=1.0, anchor="sw")

def janela_cartao_paciente(cpf_valor):

    # Cria uma nova janela para localizar as unidades médicas disponíveis
    janela_cartao_paciente = ctk.CTkToplevel()
    janela_cartao_paciente.config(bg='#161C25')
    janela_cartao_paciente.geometry('1450x1017')
    janela_cartao_paciente.resizable(False, False)
    janela_cartao_paciente.title("Cartão - Saúde Conectada")
    
    image_path = r".\midia/template.png"
    image = ctk.CTkImage(light_image= Image.open(image_path), size=(1450,300))  # Redimensionar a imagem para o tamanho da janela
    image_label = ctk.CTkLabel(janela_cartao_paciente, image=image, text="")
    image_label.place(x = 0, y =0)

    button_appearance_mode = ctk.CTkButton(master=janela_cartao_paciente, text="Mudar Tema", command=change_appearance_mode, hover_color='green')
    button_appearance_mode.pack(pady=5, padx=5)
    button_appearance_mode.place(relx=1.0, rely=0, x=-5, y=5, anchor="ne")

    image_path = r".\midia/cartao_perfil.png"
    image = ctk.CTkImage(light_image= Image.open(image_path), size=(200,200))  # Redimensionar a imagem para o tamanho da janela
    image_label = ctk.CTkLabel(janela_cartao_paciente, image=image, text='Cartão', text_color='black', width=260)
    image_label.place(x=550, y=350)

    # Criar os elementos da interface
    
    conta = db.verifica_cadastro(cpf_valor)
    #print(f'conta em questão é :{conta}')
    id_usuario = int(conta['id_usuario'][0])
    nome = str(conta['nome'][0])
    email =  str(conta['email'][0])
    senha =  str(conta['senha'][0])
    dt_nascimento =  str(conta['dt_nascimento'][0])
    telefone =  str(conta['telefone'][0])
    tipo_perfil =  str(conta['tipo_usuario'][0])

    # Convertendo a string para um objeto datetime
    data_objeto = datetime.strptime(dt_nascimento, "%Y-%m-%d")
    # Formatando a data no formato desejado
    data_formatada = data_objeto.strftime("%d/%m/%Y")

    id_label = ctk.CTkLabel(master=janela_cartao_paciente, text=f"ID: {id_usuario}")
    id_label.place(x=600, y=560)

    nome_label = ctk.CTkLabel(master=janela_cartao_paciente, text=f"Nome: {nome}")
    nome_label.place(x=600, y=600)

    email_label = ctk.CTkLabel(master=janela_cartao_paciente, text=f"Email: {email}")
    email_label.place(x=600, y=650)

    senha_label = ctk.CTkLabel(master=janela_cartao_paciente, text=f"Senha: xxxxxxx")
    senha_label.place(x=600, y=700)

    dt_nascimento_label = ctk.CTkLabel(master=janela_cartao_paciente, text=f"Data de nascimento: {data_formatada}")
    dt_nascimento_label.place(x=600, y=750)

    telefone_label = ctk.CTkLabel(master=janela_cartao_paciente, text=f"Telefone: {telefone}")
    telefone_label.place(x=600, y=800)

    tipo_perfil_label = ctk.CTkLabel(master=janela_cartao_paciente, text=f"Perfil: {tipo_perfil}")
    tipo_perfil_label.place(x=600, y=850)

    cpf_label = ctk.CTkLabel(master=janela_cartao_paciente, text=f"CPF: {cpf_valor}")
    cpf_label.place(x=600, y=900)


    #### AGORA A PARTE EDITÁVEL

    # Criando os campos editáveis
    font2 = ('Arial',12,'bold')
    
    email_entry = ctk.CTkEntry(master=janela_cartao_paciente,text_color='#000',fg_color='#fff', border_color='#0C9295', border_width=2, width=180, placeholder_text='Edite seu Email')
    email_entry.place(x=900, y=650)

    senha_entry = ctk.CTkEntry(master=janela_cartao_paciente,text_color='#000',fg_color='#fff', border_color='#0C9295', border_width=2, width=180, placeholder_text='Edite sua senha')
    senha_entry.place(x=900, y=700)

    telefone_entry = ctk.CTkEntry(master=janela_cartao_paciente,text_color='#000',fg_color='#fff', border_color='#0C9295', border_width=2, width=180, placeholder_text='Edite seu telefone')
    telefone_entry.place(x=900, y=800)


    options = ['Equipe Desenvolvimento','Médico','Paciente','Recepcionista']
    variable1 = str()

    perfil_entry = ctk.CTkComboBox(janela_cartao_paciente, font=font2, text_color='#000',fg_color='#fff', dropdown_hover_color='#0C9295', button_color='#0C9295', button_hover_color='#0C9295',border_color='#0C9295',width=180,variable=variable1, values=options, state='readonly')
    perfil_entry.set('')
    perfil_entry.place(x=900, y=850)


    # Criando um botão para salvar as alterações 
    def salvar_alteracoes():
        # Lógica para salvar as alterações no banco de dados ou em um arquivo
        novo_email =  email_entry.get()
        nova_senha =  senha_entry.get()
        novo_telefone =  telefone_entry.get()
        novo_perfil =  perfil_entry.get()

        verifica_email = format.valida_email(novo_email)

        telefone = format.format_telefone(novo_telefone)
        print(f'telefone :{telefone}')

        valida_senha = format.valida_senha(nova_senha)
        print(f'valida senha :{valida_senha}')

        if novo_email == '' and nova_senha == '' and  novo_telefone == '' and telefone == '' and novo_perfil == '':

            # Exibir uma mensagem de erro se algum campo estiver vazio
            print('Erro!! Por favor, preencha algum campo')
            label_mensagem = ctk.CTkLabel(janela_cartao_paciente, text="Erro!! Por favor, preencha algum campo", font=("Arial", 12), bg_color='#fc031c', text_color='black')
            #label_mensagem.pack(padx=10,pady=10, anchor="w")
            label_mensagem.place(x=900, y=940)
            # Após 2 segundos, remove a label da tela
            janela_cartao_paciente.after(2000, label_mensagem.destroy)
            #janela_cadastro.withdraw()

        elif novo_perfil != '':
            if tipo_perfil != 'Equipe Desenvolvimento' and tipo_perfil != 'Recepcionista':
                # Exibir uma mensagem de erro se algum campo estiver vazio
                print('Sem permissão necessária para troca')
                label_mensagem = ctk.CTkLabel(janela_cartao_paciente, text="Erro!! Sem permissão necessária para troca.", font=("Arial", 12), bg_color='#fc031c', text_color='black')
                #label_mensagem.pack(padx=10,pady=10, anchor="w")
                label_mensagem.place(x=900, y=940)
                # Após 2 segundos, remove a label da tela
                janela_cartao_paciente.after(2000, label_mensagem.destroy)
                #janela_cadastro.withdraw()
            else:
                db.atualiza_dados_cartao_tipo_perfil(id_usuario,novo_perfil)
                label_mensagem = ctk.CTkLabel(janela_cartao_paciente, text="Sucesso!! troca realizada", font=("Arial", 12), bg_color='#61eb34', text_color='black')
                label_mensagem.place(x=900, y=940)
                # Após 2 segundos, remove a label da tela
                janela_cartao_paciente.after(2000, label_mensagem.destroy)
        
        elif verifica_email == False or valida_senha == False or  telefone == False:

            # Exibir uma mensagem de erro se algum campo estiver fora do padrão necessário
            print('Algum campo está fora do padrão necessário')
            label_mensagem = ctk.CTkLabel(janela_cartao_paciente, text="Erro!! Por favor, preencha todos os campos no formato correto", font=("Arial", 12), bg_color='#fc031c', text_color='black')
            label_mensagem.place(x=900, y=940)
            # Após 2 segundos, remove a label da tela
            janela_cartao_paciente.after(2000, label_mensagem.destroy)
            #janela_cadastro.withdraw()

        if verifica_email == True and valida_senha == True and  telefone != False:
            # Botão para enviar os dados
            print(f"Novas informações salvas: {novo_email}, {nova_senha}, {novo_telefone}, {novo_perfil}")  # Exemplo de salvamento
            db.atualiza_dados_cartao(id_usuario,novo_email,nova_senha,novo_telefone)
            label_mensagem = ctk.CTkLabel(janela_cartao_paciente, text="Atualização realizada com sucesso!!", font=("Arial", 12), bg_color='#61eb34', text_color='black')
            label_mensagem.place(x=900, y=940)
            # Após 1 segundo, remove a label da tela
            janela_cartao_paciente.after(2000, label_mensagem.destroy)
            sleep(1)
            #janela_cadastro.withdraw()
            #janela_login()
            
        else:
            pass
            


            

    salvar_botao = ctk.CTkButton(master=janela_cartao_paciente, text="Salvar Alterações", command=salvar_alteracoes)
    salvar_botao.place(x=900, y=900)


    
    # Botão para enviar os dados
    botao_voltar = ctk.CTkButton(janela_cartao_paciente, text="Voltar para página principal", command=lambda: [janela_cartao_paciente.withdraw(), janela_principal(cpf_valor)], hover_color='green', width=260, text_color='black')
    botao_voltar.place(relx=0, rely=1.0, anchor="sw")


def janela_medicamentos(cpf_valor):

    # Cria uma nova janela para localizar os medicamentos disponíveis
    janela_medicamentos = ctk.CTkToplevel()
    janela_medicamentos.config(bg='#161C25')
    janela_medicamentos.geometry('1450x1017')
    janela_medicamentos.resizable(False, False)
    janela_medicamentos.title("Medicamentos disponíveis")
    
    image_path = r".\midia/template.png"
    image = ctk.CTkImage(light_image= Image.open(image_path), size=(1450,300))  # Redimensionar a imagem para o tamanho da janela
    image_label = ctk.CTkLabel(janela_medicamentos, image=image, text="")
    image_label.place(x = 0, y =0)

    button_appearance_mode = ctk.CTkButton(master=janela_medicamentos, text="Mudar Tema", command=change_appearance_mode, hover_color='green')
    button_appearance_mode.pack(pady=5, padx=5)
    button_appearance_mode.place(relx=1.0, rely=0, x=-5, y=5, anchor="ne")


    # Criar os elementos da interface
    font1 = ('Arial',20,'bold')
    font2 = ('Arial',12,'bold')

    id_label = ctk.CTkLabel(janela_medicamentos, font=font1,text='ID:',text_color='#fff',bg_color='#161C25')
    id_label.place(x=20,y=400)

    id_entry = ctk.CTkEntry(janela_medicamentos, font=font1,text_color='#000',fg_color='#fff', border_color='#0C9295', border_width=2, width=180)
    id_entry.place(x=100,y=400)

    nome_label = ctk.CTkLabel(janela_medicamentos, font=font1,text='Nome:',text_color='#fff',bg_color='#161C25')
    nome_label.place(x=20,y=480)

    nome_entry = ctk.CTkEntry(janela_medicamentos, font=font1,text_color='#000',fg_color='#fff', border_color='#0C9295', border_width=2, width=180)
    nome_entry.place(x=100,y=480)

    cargo_label = ctk.CTkLabel(janela_medicamentos, font=font1,text='Cargo:',text_color='#fff',bg_color='#161C25')
    cargo_label.place(x=20,y=560)

    cargo_entry = ctk.CTkEntry(janela_medicamentos, font=font1,text_color='#000',fg_color='#fff', border_color='#0C9295', border_width=2, width=180)
    cargo_entry.place(x=100,y=560)

    genero_label = ctk.CTkLabel(janela_medicamentos, font=font1,text='Gênero:',text_color='#fff',bg_color='#161C25')
    genero_label.place(x=20,y=640)

    options = ['Feminino','Masculino']
    variable1 = str()

    genero_options = ctk.CTkComboBox(janela_medicamentos, font=font1, text_color='#000',fg_color='#fff', dropdown_hover_color='#0C9295', button_color='#0C9295', button_hover_color='#0C9295',border_color='#0C9295',width=180,variable=variable1, values=options, state='readonly')
    genero_options.set('Male')
    genero_options.place(x=100,y=640)

    status_label = ctk.CTkLabel(janela_medicamentos, font=font1,text='Status:',text_color='#fff',bg_color='#161C25')
    status_label.place(x=20,y=730)

    status_entry = ctk.CTkEntry(janela_medicamentos, font=font1,text_color='#000',fg_color='#fff', border_color='#0C9295', border_width=2, width=180)
    status_entry.place(x=100,y=730)

    adicionar_botao = ctk.CTkButton(janela_medicamentos,font=font1,text_color='#fff',text='Adicionar', fg_color='#05A312',hover_color='#00850B',bg_color='#161C25', cursor='hand2',corner_radius=15,width=260)
    adicionar_botao.place(x=20,y=830)

    limpar_botao = ctk.CTkButton(janela_medicamentos,font=font1,text_color='#fff',text='Limpar', fg_color='#161C25',hover_color='#FF5002',bg_color='#161C25',border_color='#F15704',border_width=2,cursor='hand2',corner_radius=15,width=260)
    limpar_botao.place(x=20,y=880)

    atualizar_botao = ctk.CTkButton(janela_medicamentos,font=font1,text_color='#fff',text='Atualizar', fg_color='#161C25',hover_color='#FF5002',bg_color='#161C25',border_color='#F15704',border_width=2,cursor='hand2',corner_radius=15,width=260)
    atualizar_botao.place(x=300,y=880)

    deletar_botao = ctk.CTkButton(janela_medicamentos,font=font1,text_color='#fff',text='Deletar', fg_color='#E40404',hover_color='#AE0000',bg_color='#161C25',border_color='#E40404',border_width=2,cursor='hand2',corner_radius=15,width=260)
    deletar_botao.place(x=580,y=880)

    estilo = ttk.Style(janela_medicamentos)
    estilo.theme_use('clam')
    estilo.configure('Treeview',font=font2,foreground='#fff',background='#000', fieldbackground='#313837')
    estilo.map('Treeview',background=[('selected', '#1A8F2D')])

    tree =ttk.Treeview(janela_medicamentos,height=25)

    tree['columns'] = ('ID', 'Nome', 'Cargo', 'Genero', 'Status')

    tree.column('#0', width=0, stretch=tk.NO)
    tree.column('ID',anchor=tk.CENTER, width=200)
    tree.column('Nome',anchor=tk.CENTER, width=220)
    tree.column('Cargo',anchor=tk.CENTER, width=220)
    tree.column('Genero',anchor=tk.CENTER, width=220)
    tree.column('Status',anchor=tk.CENTER, width=220)

    tree.heading('ID', text='ID')
    tree.heading('Nome', text='Nome')
    tree.heading('Cargo', text='Cargo')
    tree.heading('Genero', text='Genero')
    tree.heading('Status', text='Status')

    tree.place(x=350,y=320)



    
    # Botão para enviar os dados
    botao_voltar = ctk.CTkButton(janela_medicamentos, text="Voltar para página principal", command=lambda: [janela_medicamentos.withdraw(), janela_principal(cpf_valor)], hover_color='green', width=260, text_color='black')
    botao_voltar.place(relx=0, rely=1.0, anchor="sw")

def janela_ouvidoria(cpf_valor):

    # Cria uma nova janela para localizar a ouvidoria
    janela_ouvidoria = ctk.CTkToplevel(fg_color='#03dffc')
    janela_ouvidoria.geometry('1450x1017')
    janela_ouvidoria.resizable(False, False)
    janela_ouvidoria.title("Ouvidoria")
    
    image_path = r".\midia/template.png"
    image = ctk.CTkImage(light_image= Image.open(image_path), size=(1450,300))  # Redimensionar a imagem para o tamanho da janela
    image_label = ctk.CTkLabel(janela_ouvidoria, image=image, text="")
    image_label.place(x = 0, y =0)

    button_appearance_mode = ctk.CTkButton(master=janela_ouvidoria, text="Mudar Tema", command=change_appearance_mode, hover_color='green')
    button_appearance_mode.pack(pady=5, padx=5)
    button_appearance_mode.place(relx=1.0, rely=0, x=-5, y=5, anchor="ne")
    
    # Cria os rótulos
    label_titulo = ctk.CTkLabel(janela_ouvidoria, text="Ouvidoria", font=("Arial", 66), text_color='yellow')
    label_numero = ctk.CTkLabel(janela_ouvidoria, text="Número da Ouvidoria: 0800 123 4567", font=("Arial", 34), text_color='yellow')
    label_informacoes = ctk.CTkLabel(janela_ouvidoria, text="Para outras informações, acesse nosso site.", font=("Arial", 34), text_color='yellow')

    # Posiciona os rótulos
    label_titulo.place(x=570, y=450)
    label_numero.place(x=435, y=570)
    label_informacoes.place(x=410, y=650)
    
    # Botão para enviar os dados
    botao_voltar = ctk.CTkButton(janela_ouvidoria, text="Voltar para página principal", command=lambda: [janela_ouvidoria.withdraw(), janela_principal(cpf_valor)], hover_color='green', width=260, text_color='black')
    botao_voltar.place(relx=0, rely=1.0, anchor="sw")


def add_to_treeview(tree):
    #employess = db.verifica_cadastro()
    tree.delete(*tree.get_children())
