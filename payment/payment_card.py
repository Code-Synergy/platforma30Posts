# cobranca.py
from flask import Blueprint, request, jsonify
import requests
from .asaas_config import HEADERS

# URL específica para pagamentos na API
PAYMENTS_URL = "https://sandbox.asaas.com/api/v3/payments"

# Blueprint para agrupar as rotas de cobranças
cobranca_bp = Blueprint('cobranca', __name__)

# Rota para criar uma nova cobrança
@cobranca_bp.route('/create', methods=['POST'])
def criar_cobranca():
    data = request.json

    # Validação básica dos campos obrigatórios
    required_fields = ["billingType", "creditCard", "creditCardHolderInfo", "customer", "value", "dueDate", "remoteIp"]
    if not all(field in data for field in required_fields):
        return jsonify({"erro": "Campos obrigatórios: billingType, creditCard, creditCardHolderInfo, customer, value, dueDate, remoteIp"}), 400

    # Fazendo a requisição para a API Asaas
    try:
        response = requests.post(PAYMENTS_URL, json=data, headers=HEADERS)
        response.raise_for_status()  # Verifica se houve erros HTTP
        api_response = response.json()

        # Retorna a resposta da API, que já estará no formato esperado
        return jsonify(api_response), 201
    except requests.exceptions.HTTPError as err:
        return jsonify({"erro": str(err)}), 500
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# Rota para listar cobranças ativas
@cobranca_bp.route('/actives', methods=['GET'])
def listar_cobrancas_ativas():
    try:
        # Fazendo a requisição GET para a API Asaas para listar cobranças ativas
        response = requests.get(PAYMENTS_URL, headers=HEADERS)
        response.raise_for_status()  # Verifica se houve erros HTTP
        api_response = response.json()

        # Filtrar apenas cobranças com status "CONFIRMED" ou "RECEIVED"
        cobrancas_ativas = [payment for payment in api_response['data'] if payment['status'] in ["CONFIRMED", "RECEIVED"]]

        # Retornando apenas as cobranças ativas
        return jsonify(cobrancas_ativas), 200
    except requests.exceptions.HTTPError as err:
        return jsonify({"erro": str(err)}), 500
    except Exception as e:
        return jsonify({"erro": str(e)}), 500