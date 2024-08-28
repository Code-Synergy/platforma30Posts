from functools import wraps
from flask import request, jsonify, current_app
import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]  # Pega o token JWT do cabeçalho

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # Decodifica o token para obter o payload
            data = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        # Passa o payload decodificado para a função protegida
        return f(*args, **kwargs, token_data=data)
    
    return decorated
