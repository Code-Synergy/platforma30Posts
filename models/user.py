from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from . import get_db

user_bp = Blueprint('user', __name__)


@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Use 'pbkdf2:sha256' para gerar o hash da senha
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO public.usuarios (username, senha, email) VALUES (%s, %s, %s);",
                (username, hashed_password, 'email@example.com'))
    conn.commit()
    cur.close()

    return jsonify({'message': 'User registered successfully'}), 201


@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT usuario_id, senha FROM public.usuarios WHERE username = %s;", (username,))
    user = cur.fetchone()
    cur.close()

    if user and check_password_hash(user[1], password):
        token = jwt.encode({
            'user_id': user[0],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401
