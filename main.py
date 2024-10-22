#.\venv\Scripts\activate 
#deactivate

from modules import janela as page



def main():
    janela = page.config()
    page.janela_login()

if __name__ == "__main__":
    main()
