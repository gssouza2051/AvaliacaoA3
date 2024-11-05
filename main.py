#.\venv\Scripts\activate 
#deactivate

from modules import janela as page

def main():
    janela = page.config()
    page.janela_login(cpf_valor=None)

if __name__ == "__main__":
    main()
