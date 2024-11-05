import pandas as pd
from sqlalchemy import create_engine
from tkinter import ttk,messagebox
from modules import acessos
import psycopg2
import tkinter as tk
from modules import format_variables as format
import datetime

def conecta_db():
    # Criando a string de conexão

    ferramenta = acessos.obter_credencial("database", "ferramenta")
    usuario = acessos.obter_credencial("database", "usuario")
    senha = acessos.obter_credencial("database", "senha")
    host = acessos.obter_credencial("database", "host")
    port = acessos.obter_credencial("database", "port")
    database = acessos.obter_credencial("database", "database")
    require = acessos.obter_credencial("database", "require")
    engine = create_engine(f"{ferramenta}://{usuario}:{senha}@{host}:{port}/{database}")
    return engine

def connect():
    ferramenta = acessos.obter_credencial("database", "ferramenta")
    usuario = acessos.obter_credencial("database", "usuario")
    senha = acessos.obter_credencial("database", "senha")
    host = acessos.obter_credencial("database", "host")
    port = acessos.obter_credencial("database", "port")
    database = acessos.obter_credencial("database", "database")


    conn = psycopg2.connect(
        host=host,
        database=database,
        user=usuario,
        password=senha,
        port=port
    )
    return conn

def read(consulta, engine):
    base = pd.read_sql_query(consulta, engine)
    return base

def write(df,table,schema, engine,payload=None):
    if payload:
        df = pd.DataFrame(data=payload, index=[0])
    df.to_sql(table, engine, schema=schema, if_exists='append', index=False)
    return True

def execute(query):
    conn = connect()
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    cur.close()

def pagina_login(cpf,senha):
    query = f'''SELECT * FROM saude.tbl_usuarios where cpf = '{cpf}' and senha = '{senha}' '''
    conn = conecta_db()
    login = read(query,conn)
    return login

def verifica_cadastro(cpf):
    query = f'''SELECT * FROM saude.tbl_usuarios where cpf = '{cpf}' '''
    conn = conecta_db()
    cadastro = read(query,conn)
    return cadastro

def cadastro_usuario(nome,email,senha,dt_nascimento,telefone,cpf):
    query = f'''
    INSERT INTO saude.tbl_usuarios (nome, email, senha, dt_nascimento, telefone, tipo_usuario, cpf)
    VALUES ('{nome}', '{email}', '{senha}', '{dt_nascimento}', '{telefone}', 'Paciente', '{cpf}');
    '''
    #print(query)
    execute(query)

def atualiza_dados_cartao(id_usuario,email,senha,telefone):
    query = f'''
    UPDATE saude.tbl_usuarios
    SET email = '{email}', senha = '{senha}',telefone = '{telefone}'
    WHERE id_usuario = {id_usuario};
    '''
    #print(query)
    execute(query)

def atualiza_dados_cartao_tipo_perfil(id_usuario,novo_tipo_usuario):
    query = f'''
    UPDATE saude.tbl_usuarios
    SET tipo_usuario = '{novo_tipo_usuario}'
    WHERE id_usuario = {id_usuario} and tipo_usuario in ('Equipe Desenvolvimento','Recepcionista');
    '''
    #print(query)
    execute(query)

def pesquisar_atendimentos(tree, nome_entry, medico_options, data_consulta_entry, horario_options, plano_saude_options, status_options, especialidade_options, cpf_valor):
    engine = conecta_db()

    #print(f'nome_entry: {nome_entry}')
    #print(f'medico_options: {medico_options}')
    print(f'data_consulta_entry: {data_consulta_entry}')
    print(f'horario_options: {horario_options}')
    print(f'especialidade_options: {especialidade_options}')
    #print(f'plano_saude_options: {plano_saude_options}')
    #print(f'status_options: {status_options}')
    #print(f'cpf:{cpf_valor}')

    data_consulta_entry = format.format_data(data_consulta_entry)
    if data_consulta_entry ==  False:
        messagebox.showerror('Erro!!',message='Insira a data no formato correto (DD/MM/YYYY)!')
    else:

        data_consulta_entry = datetime.datetime.strptime(data_consulta_entry, "%d/%m/%Y")
        data_consulta_entry = data_consulta_entry.strftime("%Y-%m-%d")
        print(f'dddd:{data_consulta_entry}')  # Saída: 2024-10-02

        confere_perfil = read(f'''select tipo_usuario from saude.tbl_usuarios where cpf = '{cpf_valor}'
                            ''', engine)
        confere_perfil = confere_perfil['tipo_usuario'][0]
        #print(f'perfil usuario :{confere_perfil}')

        if confere_perfil == 'Equipe Desenvolvimento' or confere_perfil == 'Recepcionista':
            if  medico_options == '' and plano_saude_options == '' and status_options == '' and data_consulta_entry == '' and horario_options == '' and  especialidade_options == '':
                messagebox.showerror('Erro!!',message='Selecione pelo menos os campos : Data da consulta, Especialidade,Plano de saúde, Horário, Status e médico por favor!')
            else:
                query = f'''
                    select t1.nome as paciente,t4.nome nome_medico,t2.plano_saude,to_char(t3.data_consulta, 'DD/MM/YYYY') AS data_consulta,t3.horario_consulta,t4.especialidade,t3.status
                    from saude.tbl_usuarios t1 
                    left join saude.tbl_pacientes t2 on (t1.id_usuario = t2.id_usuario)
                    left join saude.tbl_consultas t3 on (t2.id_paciente = t3.id_paciente)
                    left join saude.tbl_medicos t4 on (t3.id_medico = t4.id_medico)
                    where t3.status is not NULL
                    and t3.status = '{status_options}'
                    and t4.nome = '{medico_options}'
                    and t2.plano_saude = '{plano_saude_options}'
                    and t3.data_consulta = '{data_consulta_entry}'
                    and t3.horario_consulta = '{horario_options}'
                    and t4.especialidade = '{especialidade_options}'
                    '''
        else:
            if  medico_options == '' and plano_saude_options == '' and status_options == '':
                messagebox.showerror('Erro!!',message='Selecione pelo menos os campos : Médico, Plano de saúde e status por favor!')
            else:
                query = f'''
                    select t1.nome as paciente,t4.nome nome_medico,t2.plano_saude,to_char(t3.data_consulta, 'DD/MM/YYYY') AS data_consulta,t3.horario_consulta,t4.especialidade,t3.status
                    from saude.tbl_usuarios t1 
                    left join saude.tbl_pacientes t2 on (t1.id_usuario = t2.id_usuario)
                    left join saude.tbl_consultas t3 on (t2.id_paciente = t3.id_paciente)
                    left join saude.tbl_medicos t4 on (t3.id_medico = t4.id_medico)
                    where t3.status is not NULL
                    and t3.status = '{status_options}'
                    and t4.nome = '{medico_options}'
                    and t2.plano_saude = '{plano_saude_options}'
                    and t1.cpf = '{cpf_valor}'
                    '''
        try:
            base = read(query,engine)
            base = pd.DataFrame(base)
            base = base.values.tolist()

            for linha in base:
                tree.insert("", tk.END, values=linha)
            return base
        except:
            return []


def pesquisar_receita(tree, nome_entry, medico_options, data_consulta_entry, horario_options, cpf_valor):
    engine = conecta_db()

    #print(f'nome_entry: {nome_entry}')
    #print(f'medico_options: {medico_options}')
    #print(f'data_consulta_entry: {data_consulta_entry}')
    #print(f'horario_options: {horario_options}')
    #print(f'cpf:{cpf_valor}')

    data_consulta_entry = format.format_data(data_consulta_entry)
    if data_consulta_entry ==  False:
        messagebox.showerror('Erro!!',message='Insira a data no formato correto (DD/MM/YYYY)!')
    else:

        data_consulta_entry = datetime.datetime.strptime(data_consulta_entry, "%d/%m/%Y")
        data_consulta_entry = data_consulta_entry.strftime("%Y-%m-%d")
        #print(f'dddd:{data_consulta_entry}')  # Saída: 2024-10-02

        confere_perfil = read(f'''select tipo_usuario from saude.tbl_usuarios where cpf = '{cpf_valor}'
                            ''', engine)
        confere_perfil = confere_perfil['tipo_usuario'][0]
        #print(f'perfil usuario :{confere_perfil}')

        if confere_perfil == 'Equipe Desenvolvimento' or confere_perfil == 'Recepcionista':
            if  medico_options == ''  and data_consulta_entry == '' and horario_options == '':
                messagebox.showerror('Erro!!',message='Selecione pelo menos os campos : Data da consulta, Especialidade,Plano de saúde, Horário, Status e médico por favor!')
            else:
                query = f'''
                    select t1.nome,t6.nome medico,to_char(t3.data_consulta, 'DD/MM/YYYY') AS data_consulta,t3.horario_consulta, t4.descricao, t4.medicamentos, t5.descricao atestado
                    from saude.tbl_usuarios t1 
                    left join saude.tbl_pacientes t2 on (t1.id_usuario = t2.id_usuario)
                    left join saude.tbl_consultas t3 on (t2.id_paciente = t3.id_paciente)
                    left join saude.tbl_receitas t4 on (t3.id_consulta = t4.id_consulta)
                    left join saude.tbl_atestados t5 on (t3.id_consulta = t5.id_consulta)
                    left join saude.tbl_medicos t6 on (t1.id_usuario = t6.id_usuario)
                    where t4.medicamentos is not NULL
                    and t6.nome = '{medico_options}'
                    and t3.data_consulta = '{data_consulta_entry}'
                    and t3.horario_consulta = '{horario_options}'
                    '''
        else:
            if  medico_options == ''  and data_consulta_entry == '' and horario_options == '':
                messagebox.showerror('Erro!!',message='Selecione pelo menos os campos : Médico, Data da consulta e horário por favor!')
            else:
                query = f'''
                    select t1.nome,t6.nome medico,to_char(t3.data_consulta, 'DD/MM/YYYY') AS data_consulta,t3.horario_consulta, t4.descricao, t4.medicamentos, t5.descricao atestado
                    from saude.tbl_usuarios t1 
                    left join saude.tbl_pacientes t2 on (t1.id_usuario = t2.id_usuario)
                    left join saude.tbl_consultas t3 on (t2.id_paciente = t3.id_paciente)
                    left join saude.tbl_receitas t4 on (t3.id_consulta = t4.id_consulta)
                    left join saude.tbl_atestados t5 on (t3.id_consulta = t5.id_consulta)
                    left join saude.tbl_medicos t6 on (t1.id_usuario = t6.id_usuario)
                    where t4.medicamentos is not NULL
                    and t6.nome = '{medico_options}'
                    and t3.data_consulta = '{data_consulta_entry}'
                    and t3.horario_consulta = '{horario_options}'
                    and t1.cpf = '{cpf_valor}'
                    '''
        try:
            base = read(query,engine)
            base = pd.DataFrame(base)
            base = base.values.tolist()
            for linha in base:
                tree.insert("", tk.END, values=linha)
            return base
        except:
            return []

def update_atendimentos(tree, medico_entry, plano_entry, status_entry, data_consulta_entry, horario_entry):
    item_selecionado = tree.focus()
    if not item_selecionado:
        messagebox.showerror('Erro!!',message='nenhum item selecionado!')
    else:
        data_consulta_entry = format.format_data(data_consulta_entry)
        if data_consulta_entry ==  False:
            messagebox.showerror('Erro!!',message='Insira a data no formato correto (DD/MM/YYYY)!')
        else:
            #add_to_treeview()
            #clear()
            print('\n')
            print(f'medico:{medico_entry}')
            print(f'plano:{plano_entry}')
            print(f'status:{status_entry}')
            print(f'Data:{data_consulta_entry}')
            print(f'horario:{horario_entry}')

            query_update = '''
            
            '''

            messagebox.showinfo('Sucesso!!',message='Campos atualizados!')

def deletar_atendimentos(tree, cpf_valor):

    engine = conecta_db()
    confere_perfil = read(f'''select tipo_usuario from saude.tbl_usuarios where cpf = '{cpf_valor}'
                          ''', engine)
    confere_perfil = confere_perfil['tipo_usuario'][0]
    #print(f'perfil usuario :{confere_perfil}')

    item_selecionado = tree.focus()
    if not item_selecionado:
        messagebox.showerror('Erro!!',message='nenhum item selecionado!')
    else:
        if confere_perfil == 'Equipe Desenvolvimento' or confere_perfil == 'Recepcionista':
            print('pode excluir')
            messagebox.showinfo('Sucesso!!',message='você acabou de excluir um atendimento')
            for item in tree.get_children():
                tree.delete(item)
        
        else:
            print('nao pode excluir')
            messagebox.showerror('Sem permissão!!',message='Você não pode excluir seu próprio atendimento')

def limpar_campo(tree):

    
    item_selecionado = tree.focus()
    if not item_selecionado:
        messagebox.showerror('Erro!!',message='nenhum item selecionado!')
    else:
        messagebox.showinfo('Sucesso!!',message='você acabou de limpar um item na sua tela')
        for item in tree.get_children():
            tree.delete(item)

def adicionar_atendimentos(tree, nome_entry, medico_options, data_consulta_entry, horario_options, plano_saude_options, status_options, especialidade_options, cpf_valor):
    engine = conecta_db()

    data_consulta_entry = format.format_data(data_consulta_entry)
    if data_consulta_entry ==  False:
        messagebox.showerror('Erro!!',message='Insira a data no formato correto (DD/MM/YYYY)!')
    else:

        data_consulta_entry = datetime.datetime.strptime(data_consulta_entry, "%d/%m/%Y")
        data_consulta_entry = data_consulta_entry.strftime("%Y-%m-%d")
        #print(f'dddd:{data_consulta_entry}')  # Saída: 2024-10-02

        confere_perfil = read(f'''select tipo_usuario from saude.tbl_usuarios where cpf = '{cpf_valor}'
                            ''', engine)
        confere_perfil = confere_perfil['tipo_usuario'][0]
        #print(f'perfil usuario :{confere_perfil}')

        if confere_perfil == 'Equipe Desenvolvimento' or confere_perfil == 'Recepcionista':
            if  medico_options == '' and data_consulta_entry == '' and horario_options == '' and  especialidade_options == '':
                messagebox.showerror('Erro!!',message='Selecione pelo menos os campos : Data da consulta, Especialidade, Horário e médico por favor!')
            else:

                query_verifica_atendimento = f'''
                    select t1.nome as paciente,t4.nome nome_medico,t2.plano_saude,to_char(t3.data_consulta, 'DD/MM/YYYY') AS data_consulta,t3.horario_consulta,t4.especialidade,t3.status
                    from saude.tbl_usuarios t1 
                    left join saude.tbl_pacientes t2 on (t1.id_usuario = t2.id_usuario)
                    left join saude.tbl_consultas t3 on (t2.id_paciente = t3.id_paciente)
                    left join saude.tbl_medicos t4 on (t3.id_medico = t4.id_medico)
                    where t3.status is not NULL
                    --and t1.nome = '{nome_entry}'
                    --and t3.status = 'Pendente'
                    and t4.nome = '{medico_options}'
                    --and t2.plano_saude = '{plano_saude_options}'
                    and t3.data_consulta = '{data_consulta_entry}'
                    and t3.horario_consulta = '{horario_options}'
                    and t4.especialidade = '{especialidade_options}'
                    '''
                verifica_atendimento = read(query_verifica_atendimento, engine)
                #print(f'verificarrr:{verifica_atendimento}')
                if verifica_atendimento.empty:
                    messagebox.showinfo('Sucesso!!',message='Atendimento cadastrado com sucesso')
                else:
                    messagebox.showerror('Erro!!',message='Médico ja possui outro atendimento nessa data e horário!!')



###################################### RECEITAS #########################################################

def update_receita(tree, medico_entry, atestado_entry, medicamento_entry, descricao_entry, data_consulta_entry, horario_entry):
    item_selecionado = tree.focus()
    if not item_selecionado:
        messagebox.showerror('Erro!!',message='nenhum item selecionado!')
    else:
        data_consulta_entry = format.format_data(data_consulta_entry)
        if data_consulta_entry ==  False:
            messagebox.showerror('Erro!!',message='Insira a data no formato correto (DD/MM/YYYY)!')
        else:
            #add_to_treeview()
            #clear()
            print('\n')
            print(f'medico:{medico_entry}')
            print(f'atestado_entry:{atestado_entry}')
            print(f'medicamento_entry:{medicamento_entry}')
            print(f'descricao_entry:{descricao_entry}')
            print(f'Data:{data_consulta_entry}')
            print(f'horario:{horario_entry}')

            query_update = '''
            
            '''

            messagebox.showinfo('Sucesso!!',message='Campos atualizados!')

def deletar_receita(tree, cpf_valor):

    engine = conecta_db()
    confere_perfil = read(f'''select tipo_usuario from saude.tbl_usuarios where cpf = '{cpf_valor}'
                          ''', engine)
    confere_perfil = confere_perfil['tipo_usuario'][0]
    #print(f'perfil usuario :{confere_perfil}')

    item_selecionado = tree.focus()
    if not item_selecionado:
        messagebox.showerror('Erro!!',message='nenhum item selecionado!')
    else:
        if confere_perfil == 'Equipe Desenvolvimento' or confere_perfil == 'Recepcionista':
            print('pode excluir')
            messagebox.showinfo('Sucesso!!',message='você acabou de excluir uma receita')
            for item in tree.get_children():
                tree.delete(item)
        
        else:
            print('nao pode excluir')
            messagebox.showerror('Sem permissão!!',message='Você não pode excluir sua própria receita')


def adicionar_receita(tree, nome_entry, medico_options, data_consulta_entry, horario_options, cpf_valor):
    engine = conecta_db()

    data_consulta_entry = format.format_data(data_consulta_entry)
    if data_consulta_entry ==  False:
        messagebox.showerror('Erro!!',message='Insira a data no formato correto (DD/MM/YYYY)!')
    else:

        data_consulta_entry = datetime.datetime.strptime(data_consulta_entry, "%d/%m/%Y")
        data_consulta_entry = data_consulta_entry.strftime("%Y-%m-%d")
        #print(f'dddd:{data_consulta_entry}')  # Saída: 2024-10-02

        confere_perfil = read(f'''select tipo_usuario from saude.tbl_usuarios where cpf = '{cpf_valor}'
                            ''', engine)
        confere_perfil = confere_perfil['tipo_usuario'][0]
        #print(f'perfil usuario :{confere_perfil}')

        if confere_perfil == 'Equipe Desenvolvimento' or confere_perfil == 'Recepcionista':
            if  medico_options == ''  and data_consulta_entry == '' and horario_options == '':
                messagebox.showerror('Erro!!',message='Selecione pelo menos os campos : Data da consulta, Médico, Horário e médico por favor!')
            else:

                query_verifica_atendimento = f'''
                    select t1.nome,t6.nome medico,to_char(t3.data_consulta, 'DD/MM/YYYY') AS data_consulta,t3.horario_consulta, t4.descricao, t4.medicamentos, t5.descricao atestado
                    from saude.tbl_usuarios t1 
                    left join saude.tbl_pacientes t2 on (t1.id_usuario = t2.id_usuario)
                    left join saude.tbl_consultas t3 on (t2.id_paciente = t3.id_paciente)
                    left join saude.tbl_receitas t4 on (t3.id_consulta = t4.id_consulta)
                    left join saude.tbl_atestados t5 on (t3.id_consulta = t5.id_consulta)
                    left join saude.tbl_medicos t6 on (t1.id_usuario = t6.id_usuario)
                    where t4.medicamentos is not NULL
                    and t6.nome = '{medico_options}'
                    and t3.data_consulta = '{data_consulta_entry}'
                    and t3.horario_consulta = '{horario_options}'
                    '''
                verifica_atendimento = read(query_verifica_atendimento, engine)
                #print(f'verificarrr:{verifica_atendimento}')
                if verifica_atendimento.empty:
                    messagebox.showinfo('Sucesso!!',message='Receita cadastrada com sucesso')
                else:
                    messagebox.showerror('Erro!!',message='Receita ja existe!!')