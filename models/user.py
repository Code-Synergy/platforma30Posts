from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from . import db

# Definindo o modelo de perfis
class Perfis(db.Model):
    __tablename__ = 'perfis'

    perfil_id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), unique=True, nullable=False)


# Definindo o modelo de usuários
class Usuarios(db.Model):
    __tablename__ = 'usuarios'

    usuario_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    perfil_id = db.Column(db.Integer, db.ForeignKey('perfis.perfil_id'), nullable=True)

    # Relacionamento com a tabela Perfis
    perfil = db.relationship('Perfis', backref='usuarios')


    # Método serialize
    def serialize(self):
        return {
            'usuario_id': self.usuario_id,
            'username': self.username,
            'email': self.email
        }

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    perfil_id = data.get('perfil_id')

    # Use 'pbkdf2:sha256' para gerar o hash da senha
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    # Cria um novo usuário
    new_user = Usuarios(username=username, senha=hashed_password, email=email, perfil_id=perfil_id)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = Usuarios.query.filter_by(email=email).first()

    if user and check_password_hash(user.senha, password):
        token = jwt.encode({
            'perfil': user.perfil_id,
            'user_id': user.usuario_id,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        }, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

        return jsonify({'token': token, 'perfil': user.perfil_id}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

# Listar todos os usuários
@user_bp.route('/', methods=['GET'])
def get_user():
    """Retorna todos os usuários"""
    users = Usuarios.query.all()
    return jsonify([user.serialize() for user in users])
