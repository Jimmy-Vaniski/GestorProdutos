import sqlite3
from tkinter import *
from tkinter import ttk


class Produto:
    # Criando variavel para acessar a base de dados
    db = 'database/produtos.db'

    # Criando metodo para se conectar a base de dados
    def db_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db) as con:  # conecta com  bd
            cursor = con.cursor()  # cursor da conexão aponta para o db
            resultado = cursor.execute(consulta, parametros)  # Preparar a consulta SQL
            con.commit()  # Executar a consulta SQL preparada anteriormente
        return resultado  # Restituir o resultado da consulta SQL

    # Metodo obtem a lista de produtos
    def get_produtos(self):
        registos_tabela = self.tabela.get_children()  # Obter todos os dados da tabela
        for linha in registos_tabela:
            self.tabela.delete(linha)

        # Consulta SQL
        query = 'SELECT * FROM produto ORDER BY nome DESC'
        registos_db = self.db_consulta(query)

        # Escrever os dados no ecrã
        for linha in registos_db:
            self.tabela.insert('', 0, text=linha[1], values=linha[2])

    def validacao_nome(self):
        nome_introduzido_por_utilizador = self.nome.get()
        return len(nome_introduzido_por_utilizador) != 0

    # Melhorado para verificar se dados inseridos sao apenas numeros
    def validacao_preco(self):
        preco_introduzido_por_utilizador = self.preco.get()

        if preco_introduzido_por_utilizador == "":
            return False

        try:
            preco_convertido = round(float(preco_introduzido_por_utilizador.replace(',', '.')), 2)
            return True
        except ValueError:
            return False

    def add_produto(self):
        if self.validacao_nome() and self.validacao_preco():
            query = 'INSERT INTO produto VALUES(NULL, ?, ?)'  # Consulta SQL sem dados
            parametros = (self.nome.get(), self.preco.get())  # Parâmetros da consulta SQL
            self.db_consulta(query, parametros)
            self.mensagem['text'] = 'Produto {} adicionado com êxito'.format(self.nome.get())
            # limpar campos para novo registo
            self.nome.delete(0, END)
            self.preco.delete(0, END)
        elif self.validacao_nome() and self.validacao_preco() == False:
            self.mensagem['text'] = 'Campo obrigatório "Preço"! Vazio ou inválido '
        elif self.validacao_nome() == False and self.validacao_preco():
            self.mensagem['text'] = 'Campo obrigatório "Nome" Vazio!  '
        else:
            self.mensagem['text'] = 'Tipo de registo inválido! Revisar dados. '
        self.get_produtos()  # serve para atualizar os registos

    def del_produto(self):

        self.mensagem['text'] = ''
        try:
            self.tabela.item(self.tabela.selection())['text'][0]
        except IndexError as e:
            self.mensagem['text'] = 'Por favor, selecione um produto'
            return

        self.mensagem['text'] = ''
        nome = self.tabela.item(self.tabela.selection())['text']
        query = 'DELETE FROM produto WHERE nome = ?'  # procura pelo nome selecionado
        self.db_consulta(query, (nome,))  # apaga o que foi selecionado
        self.mensagem['text'] = 'Produto {} eliminado com êxito'.format(nome)
        self.get_produtos()  # Atualiza

    def atualizar_produtos(self, novo_nome, antigo_nome, novo_preco, antigo_preco):
        produto_modificado = False
        query = 'UPDATE produto SET nome = ?, preco = ? WHERE nome = ? AND preco = ?'
        if novo_nome != '':
            parametros = (novo_nome, antigo_preco, antigo_nome, antigo_preco)
            produto_modificado = True
        else:
            parametros = (antigo_nome, antigo_preco, antigo_nome, antigo_preco)
            produto_modificado = True

        if novo_preco != '':
            try:
                if novo_nome != '':
                    filtro = (novo_nome, novo_preco, antigo_nome, antigo_preco)
                else:
                    filtro = (antigo_nome, novo_preco, antigo_nome, antigo_preco)
                novo_preco = round(float(novo_preco.replace(',', '.')), 2)
                parametros = filtro
                produto_modificado = True
            except ValueError:
                self.mensagem['text'] = "Novo preço inválido"
                return False

        if produto_modificado:
            self.db_consulta(query, parametros)  # Executar a consulta
            self.janela_editar.destroy()  # Fechar a janela de edição de

            self.mensagem['text'] = 'O produto {} foi atualizado com êxito'.format(antigo_nome)
            self.get_produtos()  # Atualizar a tabela de produtos
        else:
            self.janela_editar.destroy()  # Fechar a janela de edição de produtos
            self.mensagem['text'] = 'O produto {} NÃO foi atualizado'.format(
                antigo_nome)  # Mostrar mensagem para o utilizador

    def edit_produto(self):
        self.mensagem['text'] = ''  # será preenchido automaticamente a mensgem
        try:
            self.tabela.item(self.tabela.selection())['text'][0]
        except IndexError as e:
            self.mensagem['text'] = 'Por favor, selecione um produto'
            return
        nome = self.tabela.item(self.tabela.selection())['text']
        old_preco = self.tabela.item(self.tabela.selection())['values'][0]  # armazena o preço anterior

        # cria uma janela pop up para alterar um item especificamente
        self.janela_editar = Toplevel()
        self.janela_editar.title = "Editar Produto"  # Título da janela
        self.janela_editar.resizable(1, 1)
        self.janela_editar.wm_iconbitmap('recursos/icon.ico')

        titulo = Label(self.janela_editar, text='Atualizar produto', font=('Calibri', 30, 'bold'))
        titulo.grid(column=0, row=0)

        frame_ep = LabelFrame(self.janela_editar, text="Editar o Produto",
                              font=('Calibri', 14, 'bold'))  # frame para editar
        frame_ep.grid(row=1, column=0, columnspan=20, pady=20)

        # Label Nome antigo
        self.etiqueta_nome_antigo = Label(frame_ep, text="Nome antigo: ",
                                          font=('Calibri', 13))  # Etiqueta de texto localizada no frame
        self.etiqueta_nome_antigo.grid(row=2, column=0)  # Posicionamento através de grid
        # apenas para mostrar o nome antigo apenas leitura
        self.input_nome_antigo = Entry(frame_ep, textvariable=StringVar(self.janela_editar, value=nome),
                                       state='readonly', font=('Calibri', 13))
        self.input_nome_antigo.grid(row=2, column=1)
        # Label Nome novo
        self.etiqueta_nome_novo = Label(frame_ep, text="Nome novo: ", font=('Calibri', 13))
        self.etiqueta_nome_novo.grid(row=3, column=0)
        # Entry Nome novo (texto que se poderá modificar)
        self.input_nome_novo = Entry(frame_ep, font=('Calibri', 13))
        self.input_nome_novo.grid(row=3, column=1)
        self.input_nome_novo.focus()  # Para que a seta do rato vá a esta Entry ao início
        # Label Preço antigo
        self.etiqueta_preco_antigo = Label(frame_ep, text="Preço antigo: ",
                                           font=('Calibri', 13))  # Etiqueta de texto localizada no frame
        self.etiqueta_preco_antigo.grid(row=4, column=0)  # Posicionamento através de grid
        # Entry Preço antigo (texto que não se poderá modificar)
        self.input_preco_antigo = Entry(frame_ep, textvariable=StringVar(self.janela_editar, value=old_preco),
                                        state='readonly', font=('Calibri', 13))
        self.input_preco_antigo.grid(row=4, column=1)
        # Label Preço novo
        self.etiqueta_preco_novo = Label(frame_ep, text="Preço novo: ", font=('Calibri', 13))
        self.etiqueta_preco_novo.grid(row=5, column=0)

        # Botão Atualizar Produto
        self.botao_atualizar = ttk.Button(frame_ep, text="Atualizar Produto", command=lambda:
        self.atualizar_produtos(self.input_nome_novo.get(), self.input_nome_antigo.get(),
                                self.input_preco_novo.get(), self.input_preco_antigo.get()))

        self.botao_atualizar.grid(row=6, columnspan=2, sticky=W + E)
        self.etiqueta_preco_novo.grid(row=5, column=0)
        # Entry Preço novo (texto que se poderá modificar)
        self.input_preco_novo = Entry(frame_ep, font=('Calibri', 13))
        self.input_preco_novo.grid(row=5, column=1)  ######
        # Botão Atualizar Produto
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        self.botao_atualizar = ttk.Button(frame_ep, text="Atualizar Produto", style='my.TButton', command=lambda:
        self.atualizar_produtos(self.input_nome_novo.get(), self.input_nome_antigo.get(),
                                self.input_preco_novo.get(), self.input_preco_antigo.get()))
        self.botao_atualizar.grid(row=6, columnspan=2, sticky=W + E)

    def __init__(self, root):
        self.janela = root
        self.janela.title("Gestor de Produtos")  # Título da janela
        self.janela.resizable(0, 0)  # Ativar o redimensionamento da janela
        self.janela.wm_iconbitmap('recursos/icon.ico')

        # Frame principal
        frame = LabelFrame(self.janela, text="Registar um novo Produto", font=('Calibri', 14, 'bold'))
        # isso corta a linha com o que se escreveu
        frame.grid(row=0, column=0, columnspan=3, pady=20)  # distancio para organizar

        # Criando label e input (entry)
        self.l_nome = Label(frame, text="Nome: ", font=('Calibri', 13))  # Etiqueta de texto localizada

        # indico em qual frame
        self.l_nome.grid(row=1, column=0)  # Posicionamento através de grid

        # criando a entry
        self.nome = Entry(frame, font=('Calibri', 13))  # Caixa de texto (input de texto) localizada no frame
        self.nome.focus()  # Para que o foco do rato vá a esta Entry no início
        self.nome.grid(row=1, column=1)

        # no mesmo frame porem na 3 linha *row2 crio label de preço
        self.l_preco = Label(frame, text="Preço: ", font=('Calibri', 13))
        self.l_preco.grid(row=2, column=0)

        # caixa de texto para o preço
        self.preco = Entry(frame, font=('Calibri', 13))
        self.preco.grid(row=2, column=1)

        # Botão Adicionar Produto
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        self.botao_adicionar = ttk.Button(frame, text="Salvar Resgisto", command=self.add_produto, style='my.TButton')
        self.botao_adicionar.grid(row=3, columnspan=2, sticky=W + E)

        # Avisos
        self.mensagem = Label(text='', fg='red', font=('Calibri', 14, 'bold'))
        self.mensagem.grid(row=3, column=0, columnspan=2, sticky=W + E)

        # Estilo para a tabela
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))  # fonte da tabela
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))  # fonte do cabeçalho
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # remove bordas

        # construindo a tabela
        self.tabela = ttk.Treeview(height=20, columns=2, style="mystyle.Treeview")
        self.tabela.grid(row=4, column=0, columnspan=2)
        self.tabela.heading('#0', text='Nome', anchor=CENTER)  # Cabeçalho da coluna nome
        self.tabela.heading('#1', text='Preço', anchor=CENTER)  # Cabeçalho da coluna preço

        # botoes para atualizar e apagar
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        botao_eliminar = ttk.Button(text='Apagar', command=self.del_produto, style='my.TButton')
        botao_eliminar.grid(row=5, column=0, sticky=W + E)
        botao_editar = ttk.Button(text='Atualizar', command=self.edit_produto, style='my.TButton')
        botao_editar.grid(row=5, column=1, sticky=W + E)

        # Chama o metodo para listar os produtos
        self.get_produtos()


if __name__ == '__main__':
    root = Tk()  # chama o objeto da classe tk
    app = Produto(root)  # envia a si mesmo para a classe produto controlando a janela root
    root.mainloop()  # mesmo sem declarar isso é um while True