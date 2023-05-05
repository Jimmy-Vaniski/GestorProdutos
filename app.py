from logging import root
from tkinter import ttk
from tkinter import *
import sqlite3


class Produto:

    def __init__(self, root):
        self.janela = root
        self.janela = root
        self.janela.title("App Gestor de Produtos")  # Título da janela
        self.janela.resizable(1, 1)  # Ativar a redimensionamento da janela. Para
        self.janela.wm_iconbitmap('recursos/icon.ico')
        # Frame principal
        frame = LabelFrame(self.janela, text="Registar um novo Produto")  # isso corta a linha com o que se escreveu
        frame.grid(row=0, column=0, columnspan=3, pady=20)  # distancio para organizar
        # Criando label e input (entry)
        self.l_nome = Label(frame, text="Nome: ")  # Etiqueta de texto localizada
        # indico em qual frame
        self.l_nome.grid(row=1, column=0)  # Posicionamento através de grid
        # criando a entry
        self.nome = Entry(frame)  # Caixa de texto (input de texto) localizada no frame
        self.nome.focus()  # Para que o foco do rato vá a esta Entry no início
        self.nome.grid(row=1, column=1)
        # no mesmo frame porem na 3 linha *row2 crio label de preço
        self.l_preco = Label(frame, text="Preço: ")
        self.l_preco.grid(row=2, column=0)
        # caixa de texto para o preço
        self.preco = Entry(frame)
        self.preco.grid(row=2, column=1)



if __name__ == '__main__':
    root = Tk()  # chama o objeto da classe tk
    app = Produto(root)  # envia a si mesmo para a classe produto controlando a janela root
    root.mainloop()  # mesmo sem declarar isso é um while True
