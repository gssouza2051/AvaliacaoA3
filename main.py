#.\venv\Scripts\activate 
#deactivate

from customtkinter import *
'''app = CTk()
app.geometry('500x400')

tabview = CTkTabview(master=app)
tabview.pack(padx=20,pady=20)

tabview.add('Tab 1')
tabview.add('Tab 2')
tabview.add('Tab 3')

label_1 = CTkLabel(master=app, text='This is tab 1')
label_1.pack(padx=20, pady=20)

label_2 = CTkLabel(master=app, text='This is tab 2')
label_2.pack(padx=20, pady=20)

label_3 = CTkLabel(master=app, text='This is tab 3')
label_3.pack(padx=20, pady=20)

app.mainloop()'''













from modules import db

def main():
    #conn = db.conecta_db()

    #base_usuarios = db.realiza_consulta_db( 'select * from saude.tbl_usuarios limit 10.', conn)
    base_usuarios = ''
    print(f'\nBase usuarios :\n{base_usuarios}')

    #base_medicos = db.realiza_consulta_db( 'select * from saude.tbl_medicos limit 10', conn)
    base_medicos = ''
    print(f'\nBase médicos :\n{base_medicos}')

    #base_pacientes = db.realiza_consulta_db( 'select * from saude.tbl_pacientes limit 10', conn)
    base_pacientes = ''
    print(f'\nBase pacientes :\n{base_pacientes}')

    #base_consultas = db.realiza_consulta_db( 'select * from saude.tbl_consultas limit 10', conn)
    base_consultas = ''
    print(f'\nBase consultas :\n{base_consultas}')

    #base_atestados = db.realiza_consulta_db( 'select * from saude.tbl_atestados limit 10', conn)
    base_atestados = ''
    print(f'\nBase atestados :\n{base_atestados}')



main()