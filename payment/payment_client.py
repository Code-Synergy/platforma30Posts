# usuarios.py
from flask import Blueprint, request, jsonify
import requests
from .asaas_config import BASE_URL, HEADERS

# Blueprint para agrupar as rotas de usuários
payment_client_bp = Blueprint('paymentClient', __name__)

# Rota para criar um novo cliente
@payment_client_bp.route('/createClient', methods=['POST'])
def criar_cliente():
    # Obtém os dados enviados na requisição
    data = request.get_json()

    # Define a URL e o payload para a criação do cliente
    url = "https://sandbox.asaas.com/api/v3/customers"
    
    payload = {
        "name": data.get("name"),
        "cpfCnpj": data.get("cpfCnpj"),
        "email": data.get("email")
    }
    

    # Faz a requisição POST à API
    response = requests.post(url, json=payload, headers=HEADERS)
    
    # Verifica se a resposta foi bem-sucedida
    if response.status_code == 200 or response.status_code == 201:
        return jsonify(response.json()), response.status_code
    else:
        # Retorna o erro em caso de falha
        return jsonify({"erro": response.text}), response.status_code

# Rota para listar todos os clientes
@payment_client_bp.route('/listClient', methods=['GET'])
def listar_clientes():
    try:
        response = requests.get(BASE_URL, headers=HEADERS)
        response.raise_for_status()
        return jsonify(response.json()), 200
    except requests.exceptions.HTTPError as err:
        return jsonify({"erro": str(err)}), 500
    except Exception as e:
        return jsonify({"erro": str(e)}), 500