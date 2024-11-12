import pandas as pd
from sqlalchemy import create_engine
from tkinter import ttk,messagebox
from modules import acessos
import psycopg2
import tkinter as tk
from modules import format_variables as format
import datetime
import openpyxl

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
    return True

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
    execute(query)

def atualiza_dados_cartao(id_usuario,email,senha,telefone):
    query = f'''
    UPDATE saude.tbl_usuarios
    SET email = '{email}', senha = '{senha}',telefone = '{telefone}'
    WHERE id_usuario = {id_usuario};
    '''
    valor = execute(query)
    return valor

def atualiza_dados_cartao_tipo_perfil(id_usuario,novo_tipo_usuario):
    query = f'''
    UPDATE saude.tbl_usuarios
    SET tipo_usuario = '{novo_tipo_usuario}'
    WHERE id_usuario = {id_usuario} and tipo_usuario in ('Equipe Desenvolvimento','Recepcionista');
    '''
    execute(query)

###################################### ATENDIMENTOS #########################################################

def pesquisar_atendimentos(tree, nome_entry, medico_options, data_consulta_entry, horario_options, plano_saude_options, status_options, especialidade_options, cpf_valor):
    engine = conecta_db()

    if  medico_options == '' or status_options == '' or data_consulta_entry == '' or horario_options == '' or  especialidade_options == '':
        messagebox.showerror('Erro!!',message='Preencha pelo menos os campos : Data da consulta, Especialidade, Horário, Status e médico por favor!')
        return 'Preencha pelo menos os campos : Data da consulta, Especialidade, Horário, Status e médico por favor!'
    
    else:
        try:
            data_consulta_entry = datetime.datetime.strptime(data_consulta_entry, "%d/%m/%Y")
            data_consulta_entry = data_consulta_entry.strftime("%Y-%m-%d")
        except:
            data_consulta_entry =  False

        if data_consulta_entry ==  False:
            messagebox.showerror('Erro!!',message='Insira a data no formato correto (DD/MM/YYYY)!')
            return 'Insira a data no formato correto (DD/MM/YYYY)!'

        #data_consulta_entry = format.format_data(data_consulta_entry)
        confere_perfil = read(f'''select tipo_usuario from saude.tbl_usuarios where cpf = '{cpf_valor}'
                            ''', engine)
        confere_perfil = confere_perfil['tipo_usuario'][0]

        if confere_perfil == 'Equipe Desenvolvimento' or confere_perfil == 'Recepcionista':
            
            query = f'''
                select t1.nome as paciente,t4.nome nome_medico,t2.plano_saude,to_char(t3.data_consulta, 'DD/MM/YYYY') AS data_consulta,t3.horario_consulta,t4.especialidade,t3.status
                from saude.tbl_usuarios t1 
                left join saude.tbl_pacientes t2 on (t1.id_usuario = t2.id_usuario)
                left join saude.tbl_consultas t3 on (t2.id_paciente = t3.id_paciente)
                left join saude.tbl_medicos t4 on (t3.id_medico = t4.id_medico)
                where t3.status is not NULL
                and t3.status = '{status_options}'
                and t4.nome = '{medico_options}'
                and t3.data_consulta = '{data_consulta_entry}'
                and t3.horario_consulta = '{horario_options}'
                and t4.especialidade = '{especialidade_options}'
                '''
        else:
            if  medico_options == '' or plano_saude_options == '' or status_options == '':
                messagebox.showerror('Erro!!',message='Preencha pelo menos os campos : Médico, Plano de saúde e status por favor!')
                return 'Preencha pelo menos os campos : Médico, Plano de saúde e status por favor!'
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
            if base.empty:
                messagebox.showerror('Sem atendimentos',message='Procuramos pelos seus filtros e não foi encontrado nenhum atendimento!')
                return 'Procuramos pelos seus filtros e não foi encontrado nenhum atendimento!'
            base = base.values.tolist()

            for linha in base:
                tree.insert("", tk.END, values=linha)
            return base
        except:
            
            return base


def update_atendimentos(tree, cpf_valor, nome_entry, medico_entry, status_entry, data_consulta_entry, horario_entry):
    engine = conecta_db()
    item_selecionado = tree.focus()
    if not item_selecionado:
        messagebox.showerror('Erro!!',message='nenhum item selecionado!')
        return 'nenhum item selecionado!'
    else:
        if nome_entry == '' or  medico_entry == '' or data_consulta_entry == '' or horario_entry == '' or  status_entry == '':
            messagebox.showerror('Erro!!',message='Preencha pelo menos os campos : Paciente,Data da consulta, Horário,médico e status por favor!')
            return 'Preencha pelo menos os campos : Paciente,Data da consulta, Horário,médico e status por favor!'
        
        else:
            try:
                data_consulta_entry = format.format_data(data_consulta_entry)
            except:
                data_consulta_entry =  False
            if data_consulta_entry ==  False:
                messagebox.showerror('Erro!!',message='Insira a data no formato correto (DD/MM/YYYY)!')
                return 'Insira a data no formato correto (DD/MM/YYYY)!'

            else:

                confere_perfil = read(f'''select tipo_usuario from saude.tbl_usuarios where cpf = '{cpf_valor}'
                            ''', engine)
                confere_perfil = confere_perfil['tipo_usuario'][0]

                if confere_perfil == 'Equipe Desenvolvimento' or confere_perfil == 'Recepcionista':

                    data_consulta_entry = datetime.datetime.strptime(data_consulta_entry, "%d/%m/%Y")
                    data_consulta_entry = data_consulta_entry.strftime("%Y-%m-%d")
                    query_verifica_atendimento = f'''
                        select t1.nome as paciente,t4.nome nome_medico,t2.plano_saude,to_char(t3.data_consulta, 'DD/MM/YYYY') AS data_consulta,t3.horario_consulta,t4.especialidade,t3.status
                        from saude.tbl_usuarios t1 
                        left join saude.tbl_pacientes t2 on (t1.id_usuario = t2.id_usuario)
                        left join saude.tbl_consultas t3 on (t2.id_paciente = t3.id_paciente)
                        left join saude.tbl_medicos t4 on (t3.id_medico = t4.id_medico)
                        where t3.status is not NULL
                        and t4.nome = '{medico_entry}'
                        and t3.data_consulta = '{data_consulta_entry}'
                        and t3.horario_consulta = '{horario_entry}'
                        '''
                    verifica_atendimento = read(query_verifica_atendimento, engine)
                    if verifica_atendimento.empty:
                        
                        id_medico = read(f"""select id_medico from saude.tbl_medicos where nome = '{medico_entry}' """, engine)
                        id_medico = id_medico['id_medico'][0]

                        try:
                            id_paciente= read(f"""select id_usuario from saude.tbl_usuarios where nome = '{nome_entry}' """, engine)
                            id_paciente = id_paciente['id_usuario'][0]
                            id_paciente = read(f"""select id_paciente from saude.tbl_pacientes where id_usuario = {id_paciente} """, engine)
                            id_paciente = id_paciente['id_paciente'][0]
                        except:
                            messagebox.showerror('Erro!!',message='Não existe esse paciente cadastrado no nosso sistema!!')
                            return 'Não existe esse paciente cadastrado no nosso sistema!!'
                    
                        query_update2 = f'''
                            UPDATE saude.tbl_consultas
                            SET horario_consulta = '{horario_entry}', data_consulta = '{data_consulta_entry}',status = '{status_entry}'
                            WHERE id_medico = {id_medico} and id_paciente = {id_paciente};
                        '''
                        execute(query_update2)
                        messagebox.showinfo('Sucesso!!',message='Atendimento atualizado com sucesso')
                        return 'Atendimento atualizado com sucesso'
                    else:
                        messagebox.showerror('Erro!!',message='Médico ja possui outro atendimento nessa data e horário!!')
                        return 'Médico ja possui outro atendimento nessa data e horário!!'
                else:
                    messagebox.showerror('Sem permissão!!',message='Você não pode atualizar nenhum atendimento')
                    return 'Você não pode atualizar nenhum atendimento'
             

def deletar_atendimentos(tree, cpf_valor, medico_options, data_consulta_entry, horario_options, status_options):

    engine = conecta_db()
    confere_perfil = read(f'''select tipo_usuario from saude.tbl_usuarios where cpf = '{cpf_valor}'
                          ''', engine)
    confere_perfil = confere_perfil['tipo_usuario'][0]

    item_selecionado = tree.focus()
    if not item_selecionado:
        messagebox.showerror('Erro!!',message='nenhum item selecionado!')
        return 'nenhum item selecionado!'
    else:
        if confere_perfil == 'Equipe Desenvolvimento' or confere_perfil == 'Recepcionista':
            try:
                data_consulta_entry = format.format_data(data_consulta_entry)
            except:
                data_consulta_entry =  False
                
            if data_consulta_entry ==  False:
                messagebox.showerror('Erro!!',message='Insira a data no formato correto (DD/MM/YYYY)!')
                return 'Insira a data no formato correto (DD/MM/YYYY)!'
            else:

                data_consulta_entry = datetime.datetime.strptime(data_consulta_entry, "%d/%m/%Y")
                data_consulta_entry = data_consulta_entry.strftime("%Y-%m-%d")

                id_medico = read(f"""select id_medico from saude.tbl_medicos where nome = '{medico_options}' """, engine)
                id_medico = id_medico['id_medico'][0]

                id_consulta = read(f"""select id_consulta from saude.tbl_consultas where id_medico = {id_medico} and data_consulta = '{data_consulta_entry}' and horario_consulta = '{horario_options}' and status = '{status_options}' """, engine)
                id_consulta = id_consulta['id_consulta'][0]

                query_delete1 = f"""DELETE FROM saude.tbl_receitas where id_consulta = {id_consulta} """
                valor = execute(query_delete1)

                query_delete2 = f"""DELETE FROM saude.tbl_atestados where id_consulta = {id_consulta} """
                valor = execute(query_delete2)

                query_delete3 = f"""DELETE FROM saude.tbl_consultas where id_medico = {id_medico} and status = '{status_options}' and horario_consulta = '{horario_options}' and data_consulta = '{data_consulta_entry}'  """
                valor = execute(query_delete3)
                messagebox.showinfo('Sucesso!!',message='você acabou de excluir um atendimento')
                for item in tree.get_children():
                    tree.delete(item)
        
        else:
            messagebox.showerror('Sem permissão!!',message='Você não pode excluir nenhum atendimento')
            return 'Você não pode excluir nenhum atendimento'

def limpar_campo(tree):

    
    item_selecionado = tree.focus()
    if not item_selecionado:
        messagebox.showerror('Erro!!',message='nenhum item selecionado!')
    else:
        messagebox.showinfo('Sucesso!!',message='você acabou de limpar um item na sua tela')
        for item in tree.get_children():
            tree.delete(item)

def adicionar_atendimentos(tree, nome_entry, medico_options, data_consulta_entry, horario_options, especialidade_options, cpf_valor):
    engine = conecta_db()

    if  medico_options == '' or data_consulta_entry == '' or horario_options == ''  or nome_entry == '' or especialidade_options == '':
        messagebox.showerror('Erro!!',message='Preencha pelo menos os campos : Data da consulta, Horário, médico, paciente  e especialidade por favor!')
        return 'Preencha pelo menos os campos : Data da consulta, Horário, médico, paciente  e especialidade por favor!'
    
    else:
        try:
            data_consulta_entry = datetime.datetime.strptime(data_consulta_entry, "%d/%m/%Y")
            data_consulta_entry = data_consulta_entry.strftime("%Y-%m-%d")
        except:
            data_consulta_entry =  False
        #data_consulta_entry = format.format_data(data_consulta_entry)
        if data_consulta_entry ==  False:
            messagebox.showerror('Erro!!',message='Insira a data no formato correto (DD/MM/YYYY)!')
            return 'Insira a data no formato correto (DD/MM/YYYY)!'

        confere_perfil = read(f'''select tipo_usuario from saude.tbl_usuarios where cpf = '{cpf_valor}'
                            ''', engine)
        confere_perfil = confere_perfil['tipo_usuario'][0]

        if confere_perfil == 'Equipe Desenvolvimento' or confere_perfil == 'Recepcionista':
            
            try:
                id_paciente= read(f"""select id_usuario from saude.tbl_usuarios where nome = '{nome_entry}' """, engine)
                id_paciente = id_paciente['id_usuario'][0]
                id_paciente = read(f"""select id_paciente from saude.tbl_pacientes where id_usuario = {id_paciente} """, engine)
                id_paciente = id_paciente['id_paciente'][0]
            except:
                messagebox.showerror('Erro!!',message='O Paciente não possui cadastro na plataforma para ter um atendimento cadastrado')
                return 'O Paciente não possui cadastro na plataforma para ter um atendimento cadastrado'
            

            id_medico = read(f"""select id_medico from saude.tbl_medicos where nome = '{medico_options}' """, engine)
            id_medico = id_medico['id_medico'][0]

            query_verifica_atendimento = f'''
                select t1.nome as paciente,t4.nome nome_medico,t2.plano_saude,to_char(t3.data_consulta, 'DD/MM/YYYY') AS data_consulta,t3.horario_consulta,t4.especialidade,t3.status
                from saude.tbl_usuarios t1 
                left join saude.tbl_pacientes t2 on (t1.id_usuario = t2.id_usuario)
                left join saude.tbl_consultas t3 on (t2.id_paciente = t3.id_paciente)
                left join saude.tbl_medicos t4 on (t3.id_medico = t4.id_medico)
                where t3.status is not NULL
                --and t3.status = 'Pendente'
                and t4.nome = '{medico_options}'
                and t3.data_consulta = '{data_consulta_entry}'
                and t3.horario_consulta = '{horario_options}'
                and t4.especialidade = '{especialidade_options}'
                '''
            verifica_atendimento = read(query_verifica_atendimento, engine)
            if verifica_atendimento.empty:
                query_cadastro_atendimento = f'''
                    INSERT INTO "saude"."tbl_consultas" ("id_paciente", "id_medico", "data_consulta", "horario_consulta", "status") VALUES
                        ({id_paciente}, {id_medico}, '{data_consulta_entry}', '{horario_options}', 'Pendente');
                '''
                execute(query_cadastro_atendimento)
                messagebox.showinfo('Sucesso!!',message='Atendimento cadastrado com sucesso')
                return 'Atendimento cadastrado com sucesso'
            else:
                messagebox.showerror('Erro!!',message='Médico ja possui outro atendimento nessa data e horário!!')
                return 'Médico ja possui outro atendimento nessa data e horário!!'
        else:
            messagebox.showerror('Sem permissão!!',message='Você não pode adicionar nenhum atendimento')
            return 'Você não pode adicionar nenhum atendimento'


###################################### RECEITAS #########################################################

def pesquisar_receita(tree, medico_options, data_consulta_entry, horario_options, cpf_valor):
    engine = conecta_db()

    if  medico_options == ''  or data_consulta_entry == '' or horario_options == '':
        messagebox.showerror('Erro!!',message='Preencha pelo menos os campos : Médico, Data da consulta e horário por favor!')
        return 'Preencha pelo menos os campos : Médico, Data da consulta e horário por favor!'
    try:
        data_consulta_entry = format.format_data(data_consulta_entry)
    except:
        data_consulta_entry =  False

    if data_consulta_entry ==  False:
        messagebox.showerror('Erro!!',message='Insira a data no formato correto (DD/MM/YYYY)!')
        return 'Insira a data no formato correto (DD/MM/YYYY)!'
    else:

        data_consulta_entry = datetime.datetime.strptime(data_consulta_entry, "%d/%m/%Y")
        data_consulta_entry = data_consulta_entry.strftime("%Y-%m-%d")

        confere_perfil = read(f'''select tipo_usuario from saude.tbl_usuarios where cpf = '{cpf_valor}'
                            ''', engine)
        confere_perfil = confere_perfil['tipo_usuario'][0]

        if confere_perfil == 'Equipe Desenvolvimento' or confere_perfil == 'Recepcionista':
            
            query = f'''
                select t1.nome,t6.nome medico,to_char(t3.data_consulta, 'DD/MM/YYYY') AS data_consulta,t3.horario_consulta, t4.descricao, t4.medicamentos, t5.descricao atestado
                from saude.tbl_usuarios t1 
                left join saude.tbl_pacientes t2 on (t1.id_usuario = t2.id_usuario)
                left join saude.tbl_consultas t3 on (t2.id_paciente = t3.id_paciente)
                left join saude.tbl_receitas t4 on (t3.id_consulta = t4.id_consulta)
                left join saude.tbl_atestados t5 on (t3.id_consulta = t5.id_consulta)
                left join saude.tbl_medicos t6 on (t3.id_medico = t6.id_medico)
                where t4.medicamentos is not NULL
                and t6.nome = '{medico_options}'
                and t3.data_consulta = '{data_consulta_entry}'
                and t3.horario_consulta = '{horario_options}'
                    '''
        else:
            if  medico_options == ''  or data_consulta_entry == '' or horario_options == '':
                messagebox.showerror('Erro!!',message='Preencha pelo menos os campos : Médico, Data da consulta e horário por favor!')
                return 'Preencha pelo menos os campos : Médico, Data da consulta e horário por favor!'
            else:
                query = f'''
                    select t1.nome,t6.nome medico,to_char(t3.data_consulta, 'DD/MM/YYYY') AS data_consulta,t3.horario_consulta, t4.descricao, t4.medicamentos, t5.descricao atestado
                    from saude.tbl_usuarios t1 
                    left join saude.tbl_pacientes t2 on (t1.id_usuario = t2.id_usuario)
                    left join saude.tbl_consultas t3 on (t2.id_paciente = t3.id_paciente)
                    left join saude.tbl_receitas t4 on (t3.id_consulta = t4.id_consulta)
                    left join saude.tbl_atestados t5 on (t3.id_consulta = t5.id_consulta)
                    left join saude.tbl_medicos t6 on (t3.id_medico = t6.id_medico)
                    where t4.medicamentos is not NULL
                    and t6.nome = '{medico_options}'
                    and t3.data_consulta = '{data_consulta_entry}'
                    and t3.horario_consulta = '{horario_options}'
                    and t1.cpf = '{cpf_valor}'
                    '''
        try:
            base = read(query,engine)
            base = pd.DataFrame(base)
            if base.empty:
                messagebox.showerror('Sem receita',message='Procuramos pelos seus filtros e não foi encontrado nenhuma receita!')
                return 'Procuramos pelos seus filtros e não foi encontrado nenhuma receita!'
            base = base.values.tolist()
            for linha in base:
                tree.insert("", tk.END, values=linha)
            return base
        except:
            return base


def update_receita(tree, cpf_valor, medico_entry, atestado_entry, medicamento_entry, descricao_entry, data_consulta_entry, horario_entry):
    engine = conecta_db()
    item_selecionado = tree.focus()
    if not item_selecionado:
        messagebox.showerror('Erro!!',message='nenhum item selecionado!')
        return 'nenhum item selecionado!'
    else:

        if  medico_entry == ''  or data_consulta_entry == '' or horario_entry == ''  or medicamento_entry == '' or atestado_entry == '':
            messagebox.showerror('Erro!!',message='Preencha pelo menos os campos : Médico, Data da consulta, horário e o medicamento por favor!')
            return 'Preencha pelo menos os campos : Médico, Data da consulta, horário e o medicamento por favor!'
        try:
            data_consulta_entry = format.format_data(data_consulta_entry)
        except:
            data_consulta_entry =  False

        if data_consulta_entry ==  False:
            messagebox.showerror('Erro!!',message='Insira a data no formato correto (DD/MM/YYYY)!')
            return 'Insira a data no formato correto (DD/MM/YYYY)!'
        else:

            confere_perfil = read(f'''select tipo_usuario from saude.tbl_usuarios where cpf = '{cpf_valor}'
                        ''', engine)
            confere_perfil = confere_perfil['tipo_usuario'][0]

            if confere_perfil == 'Equipe Desenvolvimento' or confere_perfil == 'Recepcionista':

                data_consulta_entry = datetime.datetime.strptime(data_consulta_entry, "%d/%m/%Y")
                data_consulta_entry = data_consulta_entry.strftime("%Y-%m-%d")
                query_verifica_receita = f'''
                    select t1.nome,t6.nome medico,to_char(t3.data_consulta, 'DD/MM/YYYY') AS data_consulta,t3.horario_consulta,t4.medicamentos,t4.descricao, t5.descricao atestado
                    from saude.tbl_usuarios t1 
                    left join saude.tbl_pacientes t2 on (t1.id_usuario = t2.id_usuario)
                    left join saude.tbl_consultas t3 on (t2.id_paciente = t3.id_paciente)
                    left join saude.tbl_receitas t4 on (t3.id_consulta = t4.id_consulta)
                    left join saude.tbl_atestados t5 on (t3.id_consulta = t5.id_consulta)
                    left join saude.tbl_medicos t6 on (t3.id_medico = t6.id_medico)
                    where t4.medicamentos is not NULL
                    and t4.medicamentos = '{medicamento_entry}'
                    and t5.descricao = 'Atestado de {atestado_entry}'
                    and t6.nome = '{medico_entry}'
                    and t3.data_consulta = '{data_consulta_entry}'
                    and t3.horario_consulta = '{horario_entry}'
                    '''
                verifica_receita = read(query_verifica_receita, engine)
                if verifica_receita.empty:

                    if  descricao_entry == '' or medicamento_entry == '':
                        messagebox.showerror('Erro!!',message='Preencha pelo menos os campos : medicamento e a descrição por favor!')
                        return 'Preencha pelo menos os campos : medicamento e a descrição por favor!'

                    query_update = f'''
                        UPDATE saude.tbl_receitas
                        SET medicamentos = '{medicamento_entry}', descricao = '{descricao_entry}'
                        WHERE  data_emissao = '{data_consulta_entry}';
                    '''
                    execute(query_update)
                    messagebox.showinfo('Sucesso!!',message='Receita atualizada com sucesso')
                    return 'Receita atualizada com sucesso'
                else:
                    messagebox.showerror('Erro!!',message='Já possui uma receita cadastrada com esses filtros!!')
                    return 'Já possui uma receita cadastrada com esses filtros!!'
            else:
                messagebox.showerror('Sem permissão!!',message='Você não pode atualizar nenhuma receita')
                return 'Você não pode atualizar nenhuma receita'

def deletar_receita(tree, cpf_valor, medico_options, data_consulta_entry, horario_options):

    engine = conecta_db()
    confere_perfil = read(f'''select tipo_usuario from saude.tbl_usuarios where cpf = '{cpf_valor}'
                          ''', engine)
    confere_perfil = confere_perfil['tipo_usuario'][0]

    item_selecionado = tree.focus()
    if not item_selecionado:
        messagebox.showerror('Erro!!',message='nenhum item selecionado!')
        return 'nenhum item selecionado!'
    else:
        if confere_perfil == 'Equipe Desenvolvimento' or confere_perfil == 'Recepcionista':
            try:
                data_consulta_entry = format.format_data(data_consulta_entry)
            except:
                data_consulta_entry =  False

            if data_consulta_entry ==  False:
                messagebox.showerror('Erro!!',message='Insira a data no formato correto (DD/MM/YYYY)!')
                return 'Insira a data no formato correto (DD/MM/YYYY)!'
            else:

                data_consulta_entry = datetime.datetime.strptime(data_consulta_entry, "%d/%m/%Y")
                data_consulta_entry = data_consulta_entry.strftime("%Y-%m-%d")

                id_medico = read(f"""select id_medico from saude.tbl_medicos where nome = '{medico_options}' """, engine)
                id_medico = id_medico['id_medico'][0]
 
                id_consulta = read(f"""select id_consulta from saude.tbl_consultas where id_medico = {id_medico} and data_consulta = '{data_consulta_entry}' and horario_consulta = '{horario_options}' """, engine)
                id_consulta = id_consulta['id_consulta'][0]

                query_delete1 = f"""DELETE FROM saude.tbl_receitas where id_consulta = {id_consulta} """
                valor = execute(query_delete1)

                query_delete2 = f"""DELETE FROM saude.tbl_atestados where id_consulta = {id_consulta} """
                valor = execute(query_delete2)

                query_delete3 = f"""DELETE FROM saude.tbl_consultas where id_medico = {id_medico} and horario_consulta = '{horario_options}' and data_consulta = '{data_consulta_entry}'  """
                valor = execute(query_delete3)
                messagebox.showinfo('Sucesso!!',message='você acabou de excluir uma receita')
                for item in tree.get_children():
                    tree.delete(item)
        
        else:
            messagebox.showerror('Sem permissão!!',message='Você não pode excluir nenhuma receita')
            return 'Você não pode excluir nenhuma receita'


def adicionar_receita(tree, nome_entry, medico_options, medicamento_entry, atestado_entry, descricao_entry, data_consulta_entry, horario_options, cpf_valor):
    engine = conecta_db()

    if nome_entry == '' or  medico_options == '' or medicamento_entry == '' or atestado_entry == '' or descricao_entry == '' or data_consulta_entry == '' or horario_options == '':
        messagebox.showerror('Erro!!',message='Preencha todos os campos por favor')
        return 'Preencha todos os campos por favor'
    try:
        data_consulta_entry = format.format_data(data_consulta_entry)
    except:
        data_consulta_entry =  False

    if data_consulta_entry ==  False:
        messagebox.showerror('Erro!!',message='Insira a data no formato correto (DD/MM/YYYY)!')
        return 'Insira a data no formato correto (DD/MM/YYYY)!'
    else:

        data_consulta_entry = datetime.datetime.strptime(data_consulta_entry, "%d/%m/%Y")
        data_consulta_entry = data_consulta_entry.strftime("%Y-%m-%d")

        confere_perfil = read(f'''select tipo_usuario from saude.tbl_usuarios where cpf = '{cpf_valor}'
                            ''', engine)
        confere_perfil = confere_perfil['tipo_usuario'][0]

        if confere_perfil == 'Equipe Desenvolvimento' or confere_perfil == 'Recepcionista':

            query_verifica_receita = f'''
                select t1.nome,t6.nome medico,to_char(t3.data_consulta, 'DD/MM/YYYY') AS data_consulta,t3.horario_consulta,t4.medicamentos,t4.descricao, t5.descricao atestado, t4.data_emissao,t3.id_consulta
                from saude.tbl_usuarios t1 
                left join saude.tbl_pacientes t2 on (t1.id_usuario = t2.id_usuario)
                left join saude.tbl_consultas t3 on (t2.id_paciente = t3.id_paciente)
                left join saude.tbl_receitas t4 on (t3.id_consulta = t4.id_consulta)
                left join saude.tbl_atestados t5 on (t3.id_consulta = t5.id_consulta)
                left join saude.tbl_medicos t6 on (t3.id_medico = t6.id_medico)
                where t4.medicamentos is not NULL
                and t6.nome = '{medico_options}'
                and t3.data_consulta = '{data_consulta_entry}'
                and t3.horario_consulta = '{horario_options}'
                '''
            verifica_receita = read(query_verifica_receita, engine)
            if verifica_receita.empty:

                id_consulta = read(f"""select id_consulta from saude.tbl_consultas order by id_consulta desc limit 1 """, engine)
                id_consulta = id_consulta['id_consulta'][0]
                id_consulta = int(id_consulta) + 1
                
                id_medico = read(f"""select id_medico from saude.tbl_medicos where nome = '{medico_options}' """, engine)
                id_medico = id_medico['id_medico'][0]

                try:
                    id_paciente= read(f"""select id_usuario from saude.tbl_usuarios where nome = '{nome_entry}' """, engine)
                    id_paciente = id_paciente['id_usuario'][0]
                    id_paciente = read(f"""select id_paciente from saude.tbl_pacientes where id_usuario = {id_paciente} """, engine)
                    id_paciente = id_paciente['id_paciente'][0]
                except:
                    messagebox.showerror('Erro!!',message='Não existe esse paciente cadastrado no nosso sistema!!')
                    return 'Não existe esse paciente cadastrado no nosso sistema!!'

                
                query_adiciona_consulta = f'''
                        INSERT INTO "saude"."tbl_consultas" ("id_consulta", "id_paciente", "id_medico", "data_consulta", "horario_consulta", "status") VALUES
                        ({id_consulta}, {id_paciente}, {id_medico}, '{data_consulta_entry}', '{horario_options}', 'Pendente');
                '''

                query_adiciona_receita = f'''
                    INSERT INTO "saude"."tbl_receitas" ("id_consulta", "descricao", "medicamentos", "data_emissao") VALUES
                    ({id_consulta}, '{descricao_entry}', '{medicamento_entry}', '{data_consulta_entry}');
                '''

                query_adiciona_atestado = f'''
                    INSERT INTO "saude"."tbl_atestados" ("id_consulta", "descricao", "data_emissao") VALUES
                    ({id_consulta}, 'Atestado de {atestado_entry}', '{data_consulta_entry}');
                '''
                execute(query_adiciona_consulta)
                execute(query_adiciona_receita)
                execute(query_adiciona_atestado)
                messagebox.showinfo('Sucesso!!',message='Receita cadastrada com sucesso')
                return 'Receita cadastrada com sucesso'
            else:
                messagebox.showerror('Erro!!',message='Receita ja existe!!')
                return 'Receita ja existe!!'
            
        else:
            messagebox.showerror('Sem permissão!!',message='Você não pode adicionar nenhuma receita')
            return 'Você não pode adicionar nenhuma receita'


###### CASO PRECISE DAS BASES

def query_tbl_atestados():
    query = f'''SELECT * FROM saude.tbl_atestados '''
    conn = conecta_db()
    base = read(query,conn)
    print('\n')
    print(f'base atestados:\n{base}')
    base.to_excel(r'C:\Users\biel_\OneDrive\Documentos/tbl_atestados.xlsx', index=False)
    return base

def query_tbl_consultas():
    query = f'''SELECT * FROM saude.tbl_consultas '''
    conn = conecta_db()
    base = read(query,conn)
    print('\n')
    print(f'base consultas:\n{base}')
    base.to_excel(r'C:\Users\biel_\OneDrive\Documentos/tbl_consultas.xlsx')
    return base

def query_tbl_medicos():
    query = f'''SELECT * FROM saude.tbl_medicos '''
    conn = conecta_db()
    base = read(query,conn)
    print('\n')
    print(f'base medicos:\n{base}')
    base.to_excel(r'C:\Users\biel_\OneDrive\Documentos/tbl_medicos.xlsx')
    return base

def query_tbl_pacientes():
    query = f'''SELECT * FROM saude.tbl_pacientes '''
    conn = conecta_db()
    base = read(query,conn)
    print('\n')
    print(f'base pacientes:\n{base}')
    base.to_excel(r'C:\Users\biel_\OneDrive\Documentos/tbl_pacientes.xlsx')
    return base

def query_tbl_receitas():
    query = f'''SELECT * FROM saude.tbl_receitas '''
    conn = conecta_db()
    base = read(query,conn)
    print('\n')
    print(f'base receitas:\n{base}')
    base.to_excel(r'C:\Users\biel_\OneDrive\Documentos/tbl_receitas.xlsx')
    return base

def query_tbl_usuarios():
    query = f'''SELECT * FROM saude.tbl_usuarios '''
    conn = conecta_db()
    base = read(query,conn)
    print('\n')
    print(f'base usuarios:\n{base}')
    base.to_excel(r'C:\Users\biel_\OneDrive\Documentos/tbl_usuarios.xlsx')
    return base

def query_historico_atendimentos():
    query = f'''
    select t1.nome paciente,t4.nome nome_medico,t2.plano_saude,to_char(t3.data_consulta, 'DD/MM/YYYY') AS data_consulta,t3.horario_consulta,t4.especialidade,t3.status
    from saude.tbl_usuarios t1 
    left join saude.tbl_pacientes t2 on (t1.id_usuario = t2.id_usuario)
    left join saude.tbl_consultas t3 on (t2.id_paciente = t3.id_paciente)
    left join saude.tbl_medicos t4 on (t3.id_medico = t4.id_medico)
    where t3.status is not NULL
    '''
    conn = conecta_db()
    base = read(query,conn)
    print('\n')
    print(f'base Histórico Atendimentos:\n{base}')
    base.to_excel(r'C:\Users\biel_\OneDrive\Documentos/tbl_historico_atendimentos.xlsx')
    return base

def query_historico_receitas():
    query = f'''
        select t1.nome,t6.nome medico,to_char(t3.data_consulta, 'DD/MM/YYYY') AS data_consulta,t3.horario_consulta,t4.medicamentos,t4.descricao, t5.descricao atestado, t4.data_emissao,t3.id_consulta
        from saude.tbl_usuarios t1 
        left join saude.tbl_pacientes t2 on (t1.id_usuario = t2.id_usuario)
        left join saude.tbl_consultas t3 on (t2.id_paciente = t3.id_paciente)
        left join saude.tbl_receitas t4 on (t3.id_consulta = t4.id_consulta)
        left join saude.tbl_atestados t5 on (t3.id_consulta = t5.id_consulta)
        left join saude.tbl_medicos t6 on (t3.id_medico = t6.id_medico)
        where t4.medicamentos is not NULL
        '''
    conn = conecta_db()
    base = read(query,conn)
    print('\n')
    print(f'base Histórico Receitas:\n{base}')
    base.to_excel(r'C:\Users\biel_\OneDrive\Documentos/tbl_historico_receitas.xlsx')
    return base

'''query_tbl_atestados()
query_tbl_consultas()
query_tbl_medicos()
query_tbl_pacientes()
query_tbl_receitas()
query_tbl_usuarios()
query_historico_atendimentos()
query_historico_receitas()'''