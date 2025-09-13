from flask import Flask, jsonify, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from datetime import datetime
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estoque.db'
app.config['SECRET_KEY'] = 'sua_chave_secreta'

# Extensões
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
@app.route("/")
def home():
    # manda a pessoa para o endpoint 'login'
    return redirect(url_for("login"))


# Modelos
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    validade = db.Column(db.Date, nullable=False)

def seed_if_empty():
    if Produto.query.count() == 0:
        itens = [
            Produto(nome="X-Burger",        preco=15.00, quantidade=0, validade=datetime(2025, 12, 31)),
            Produto(nome="Coca-Cola 350ml", preco=6.00,  quantidade=0, validade=datetime(2025, 12, 31)),
            Produto(nome="Batata Frita",    preco=12.00, quantidade=0, validade=datetime(2025, 12, 31)),
        ]
        db.session.add_all(itens)
        db.session.commit()

# Login
def login_requerido(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            return jsonify({'erro': 'Login requerido'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route("/login", methods=["GET", "POST"])  
def login():
    if request.method == "POST":
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        usuario = Usuario.query.filter_by(username=username).first()
        if usuario and usuario.check_password(password):
            session["usuario_id"] = usuario.id
            return jsonify({"mensagem": "Login realizado com sucesso"}), 200
        else:
            return jsonify({"erro": "Usuário ou senha inválidos"}), 401

    # >>> esse trecho trata o GET (linha nova abaixo do if)
    return jsonify({"mensagem": "Página de login - use POST para autenticar"}), 200

@app.route('/logout', methods=['GET','POST'])
def logout():
    session.pop('usuario_id', None)
    return jsonify({'mensagem': 'Logout realizado com sucesso'}), 200


# Listar produtos
@app.route('/produtos', methods=['GET'])
@login_requerido
def listar_produtos():
    produtos = Produto.query.all()
    lista = [
        {
            'id': p.id,
            'nome': p.nome,
            'quantidade': p.quantidade,
            'preco': p.preco,
            'validade': p.validade.strftime('%Y-%m-%d')
        } for p in produtos
    ]
    return jsonify(lista), 200

# Adicionar produtos
@app.route('/produtos', methods=['POST'])
@login_requerido
def add_produto():
    data = request.get_json()

    try:
        nome = data['nome']
        quantidade = int(data['quantidade'])
        preco = float(str(data['preco']).replace(',', '.'))
        validade = datetime.strptime(data['validade'], '%Y-%m-%d').date()

        if quantidade <= 0 or preco < 0:
            return jsonify({'erro': 'Quantidade e preço devem ser positivos'}), 400

    except (KeyError, ValueError):
        return jsonify({'erro': 'Dados inválidos ou ausentes'}), 400

    novo_produto = Produto(
        nome=nome,
        quantidade=quantidade,
        preco=preco,
        validade=validade  
    )
    db.session.add(novo_produto)
    db.session.commit()
    return jsonify({
        "id": novo_produto.id,
        "mensagem": "Produto adicionado com sucesso"
    }), 201



# Editar produtos
@app.route('/produtos/<int:id>', methods=['PUT'])
@login_requerido
def editar_produto(id):
    produto = Produto.query.get_or_404(id)
    data = request.get_json()

    try:
        produto.quantidade = int(data['quantidade'])
        produto.preco = float(str(data['preco']).replace(',', '.'))
        produto.validade = datetime.strptime(data['validade'], '%Y-%m-%d').date()

        if produto.quantidade <= 0 or produto.preco < 0:
            return jsonify({'erro': 'Quantidade e preço devem ser positivos'}), 400
    except (KeyError, ValueError):
        return jsonify({'erro': 'Dados inválidos ou ausentes'}), 400    

# PUT - atualizar produto
@app.route('/produtos/<int:id>', methods=['PUT'])
@login_requerido
def atualizar_produto(id):
    data = request.get_json()
    produto = Produto.query.get_or_404(id)
    produto.nome = data.get("nome", produto.nome)
    produto.quantidade = int(data.get("quantidade", produto.quantidade))
    produto.preco = float(data.get("preco", produto.preco))
    produto.validade = datetime.strptime(
        data.get("validade", produto.validade.strftime("%Y-%m-%d")),
        "%Y-%m-%d"
    ).date()
    db.session.commit()
    return jsonify({
        "id": produto.id,
        "mensagem": "Produto atualizado com sucesso",
        "novo": {
            "nome": produto.nome,
            "quantidade": produto.quantidade,
            "preco": produto.preco,
            "validade": produto.validade.isoformat()
        }
    }), 200

# Deletar produto
@app.route('/produtos/<int:id>', methods=['DELETE'])
@login_requerido
def delete_produto(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    return jsonify({"mensagem": "Produto deletado com sucesso"}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_if_empty()  # popula X-Burger, Coca-Cola, Batata Frita se estiver vazio
    app.run(host="0.0.0.0", port=8080)
