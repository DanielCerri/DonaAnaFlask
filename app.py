from flask import Flask,g,render_template,request,redirect,url_for,flash,session,send_from_directory
from models.database import Database
import os
from models.classproduto import Produto
#import smtplib

app = Flask(__name__)

app.secret_key="DS1BACKEND"

base_dir = os.path.abspath(os.path.dirname(__file__))

# Define o UPLOAD_FOLDER combinando o base_dir com a pasta 'uploads'
UPLOAD_FOLDER = os.path.join(base_dir, 'uploads')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DEBUG'] = True





#Configurando o metodo magico do flask para automaticamente fechar conexao
# com o banco de dados
@app.teardown_appcontext
def close_connection(exception):
    db_conn = g.pop('db',None)
    if db_conn is not None:
        db_conn.close()
        print("CONEXÃO ENCERRADA COM SUCESSO!!")

banco = Database()

def tables():
    banco.execute_non_query(r"""
    CREATE TABLE IF NOT EXISTS MESA(
    id integer primary key autoincrement,
    comanda varchar(255)
    );
 """)
    
    banco.execute_non_query(r"""
    CREATE TABLE IF NOT EXISTS CARDAPIO(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto varchar(255),
    preco  REAL(10,2),
    descricao varchar(255),
    categoria varchar(50),
    pastaimagem varchar(255),
    nomeimagem varchar(255)                  
                            );
 """)


    banco.execute_non_query(r"""
    CREATE TABLE IF NOT EXISTS Usuarios(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario varchar(255),
    senha varchar(500)  
    );                    
    """)

    banco.execute_non_query(r"""
    CREATE TABLE IF NOT EXISTS ITEM_MESA(
    id_mesa integer ,
    id_item integer,
    status varchar(20),
    FOREIGN KEY("id_mesa") references mesa ("id"),
    FOREIGN KEY("id_item") references cardapio ("id")                        
    );
 """)





@app.route("/")
def index():
    tables()
    return render_template('restaurante.html')




@app.route("/gestor")
def gestor():
    return render_template('login.html')


#autenticar login 
@app.route("/login",methods=["POST"])
def entrar():
    username = request.form["username"]
    senha = request.form["password"]
    
    dados = banco.execute_query(r"""
    SELECT * FROM USUARIOS WHERE usuario=? and senha =?""",username,senha)

    if dados:
        session['username']=username # Crio a sessão com o email da conta!
        return redirect(url_for("painel"))
    else:
        flash("EMAIL OU SENHA INCORRETOS")
        return redirect(url_for("gestor"))
    
@app.route("/logout")
def logout():
    session.pop("username")
    return redirect(url_for('gestor'))

    
@app.route("/cadastrar_produto",methods=['POST'])
def cadastrar_produto():
    obj = Produto()
    obj.produto=request.form.get("nome_produto")
    obj.descricao=request.form.get("descricao_produto")
    obj.preco=request.form.get("preco_produto") 
    obj.categoria=request.form.get("categoria_produto")  

    banco.execute_non_query(r"""
    INSERT INTO CARDAPIO (PRODUTO,PRECO,CATEGORIA,DESCRICAO) VALUES(?,?,?,?)
 """,obj.produto,obj.preco,obj.categoria,obj.descricao)

    return redirect(url_for('painel'))

@app.route("/painel")
def painel():

    if session.get("username"):
        cardapio=banco.execute_query(r"""
        SELECT * FROM CARDAPIO;""")
    
        return render_template('painel.html',cardapio = cardapio)
    else:
        flash("Voce precisa realizar o login !")
        return redirect(url_for('gestor'))



@app.route("/pedidos")
def pedidos ():
    return render_template('pedidos.html')


@app.route("/criar_mesa")
def criar_mesa():
    return render_template('fazerpedido.html')


app.route("mesa")
def mesa():
    return ""

@app.route("/revisar_pedido",methods=['POST'])
def revisar_pedido():
    return render_template('revisarpedido.html')