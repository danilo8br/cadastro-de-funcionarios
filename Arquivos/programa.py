from PyQt5 import uic, QtWidgets
from pymongo import MongoClient, errors
from bson.objectid import ObjectId
from bson import errors as beeros

# Inicializando a aplicação
app=QtWidgets.QApplication([])

def conectar():
    """
    Função para conectar no banco de dados
    """
    conn = MongoClient('localhost', 27017)
    return conn


def desconectar(conn):
    """
    Função para desconectar do banco de dados
    :param conn: se tiver conexão com o banco de dados, será desconectado
    """
    if conn:
        conn.close()


def cadastrar(): 
    """
    Função inserir dados no mongo
    """
    conn = conectar()
    db = conn.pymongo

    nome = str(primeira_tela.lineEdit.text())
    idade = int(primeira_tela.lineEdit_2.text())
    cargo = str(primeira_tela.lineEdit_3.text())
    endereço = str(primeira_tela.lineEdit_4.text())
    try:
        db.funcionarios.insert_one(
            { 
                'nome': nome,
                'idade': idade,
                'cargo': cargo,
                'endereço': endereço,
            }
        )
        primeira_tela.close()
        segunda_tela.show()
    except:
        primeira_tela.label.setText('Não foi possível inserir dados.')
    desconectar(conn)


def listar():
    """
    Função para listar os dados
    """
    conn = conectar()
    db = conn.pymongo
    try:
        if db.funcionarios.count_documents({}) > 0:
            produtos = db.funcionarios.find()
            for produto in produtos:
                terceira_tela.listWidget.addItem(str(produto))
            primeira_tela.close()
            terceira_tela.show()
        else: 
            primeira_tela.close()
            quarta_tela.show()
    except errors.PyMongoError as e:
        print(f'Erro ao acessar o banco de dados: {e}')
    desconectar(conn)

def redirecionar_para_alterar():
    """
    Função para redirecionar para tela de alterar os dados
    """
    primeira_tela.close()
    quinta_tela.show()

def alterar():
    """
    Função para alterar os dados
    """
    conn = conectar()
    db = conn.pymongo
    nome = str(quinta_tela.lineEdit_6.text())
    idade = (quinta_tela.lineEdit_7.text())
    cargo = str(quinta_tela.lineEdit_8.text())
    endereço = str(quinta_tela.lineEdit_9.text())
    try:
        if db.funcionarios.count_documents({}) > 0:
            res = db.funcionarios.update_one(
                {"nome": nome},
                {
                    '$set': {
                        'idade': idade,
                        'cargo': cargo,
                        'endereço': endereço
                    }
                }
            )   

            if res.modified_count == 1:
                quinta_tela.close()
                sexta_tela.show() 
            else:
                print('Erro')
    except errors.PyMongoError as e:
        print(f'Erro ao acessar o banco de dados: {e}')
    desconectar(conn)


def redirecionar_para_deletar():
    """
    Função para redirecionar para a tela de deletar os dados
    """
    primeira_tela.close()
    setima_tela.show()


def deletar():
    """
    Função para deletar os dados
    """
    conn = conectar()
    db = conn.pymongo

    nome = str(setima_tela.lineEdit.text())
    try:
        if db.funcionarios.count_documents({}) > 0:
            res = db.funcionarios.delete_one(
                {
                    'nome': nome
                }
            )
            if res.deleted_count > 0:
                setima_tela.close()
                oitava_tela.show()
            else:
                print('Não foi possivel deletar o funcionario')
        else:
            print('Não existem dados para serem deletados.')
    except errors.PyMongoError as e:
        print(f'Erro ao acessar o  banco de dados: {e}')
    desconectar(conn)    

def logout():
    """
    Função para voltar para tela principal
    """
    segunda_tela.close()
    terceira_tela.close()
    quarta_tela.close()
    quinta_tela.close()
    sexta_tela.close()
    setima_tela.close()
    oitava_tela.close()
    primeira_tela.show()

# Carregando os arquivos
primeira_tela = uic.loadUi('primeira_tela.ui')
segunda_tela = uic.loadUi('segunda_tela.ui')
terceira_tela = uic.loadUi('terceira_tela.ui')
quarta_tela = uic.loadUi('quarta_tela.ui')
quinta_tela = uic.loadUi('quinta_tela.ui')
sexta_tela = uic.loadUi('sexta_tela.ui')
setima_tela = uic.loadUi('setima_tela.ui')
oitava_tela = uic.loadUi('oitava_tela.ui')
# Mostrando a primeira tela
primeira_tela.show()
# Botões
primeira_tela.pushButton_5.clicked.connect(cadastrar)
primeira_tela.pushButton_2.clicked.connect(listar)
primeira_tela.pushButton_3.clicked.connect(redirecionar_para_alterar)
quinta_tela.pushButton_6.clicked.connect(alterar)
primeira_tela.pushButton_4.clicked.connect(redirecionar_para_deletar)
setima_tela.pushButton_6.clicked.connect(deletar)
segunda_tela.pushButton_5.clicked.connect(logout)
terceira_tela.pushButton_5.clicked.connect(logout)
quarta_tela.pushButton_5.clicked.connect(logout)
sexta_tela.pushButton_5.clicked.connect(logout)
oitava_tela.pushButton_5.clicked.connect(logout)
# Executando a apliucação
app.exec()



