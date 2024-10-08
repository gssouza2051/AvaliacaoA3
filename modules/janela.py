#.\venv\Scripts\activate 
#deactivate

import customtkinter

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')

janela = customtkinter.CTk()
janela.geometry('500x300')

def login():
    print('Login feito')

texto = customtkinter.CTkLabel(janela, text='Fazer Login')
texto.pack(padx=10,pady=10)

cpf = customtkinter.CTkEntry(janela, placeholder_text='Seu CPF')
cpf.pack(padx=10,pady=10)

senha = customtkinter.CTkEntry(janela, placeholder_text='Sua senha', show='*')
senha.pack(padx=10,pady=10)

checkbox = customtkinter.CTkCheckBox(janela, text='Lembrar Login')
checkbox.pack(padx=10,pady=10)

botao = customtkinter.CTkButton(janela, text='Login', command=login)
botao.pack(padx=10,pady=10)

janela.mainloop()


