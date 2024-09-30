import requests
from flask import Flask, request, jsonify, Blueprint

paymentJ_bp = Blueprint('paymentJ', __name__)

ASAAS_URL = 'https://sandbox.asaas.com/api/v3/customers'
ACCESS_TOKEN = '$aact_YTU5YTE0M2M2N2I4MTliNzk0YTI5N2U5MzdjNWZmNDQ6OjAwMDAwMDAwMDAwMDAwOTA2NDY6OiRhYWNoXzU0MTg4NmY0LTNhNTEtNDJmYi04ZmM2LThjMWM3YzZlODlhYw=='
 # JEAN '$aact_YTU5YTE0M2M2N2I4MTliNzk0YTI5N2U5MzdjNWZmNDQ6OjAwMDAwMDAwMDAwMDA0OTE1NjM6OiRhYWNoXzlkODUyOTQ2LTJhMDktNDMyNC05YTQ5LWI1MDRkZjAyYTI0OA=='

# JAPA '$aact_YTU5YTE0M2M2N2I4MTliNzk0YTI5N2U5MzdjNWZmNDQ6OjAwMDAwMDAwMDAwMDAwOTA2NDY6OiRhYWNoXzU0MTg4NmY0LTNhNTEtNDJmYi04ZmM2LThjMWM3YzZlODlhYw=='


@paymentJ_bp.route('/customer/<cpf_cnpj>', methods=['GET'])
def get_customer(cpf_cnpj):
    headers = retornaHead()

    # Realizar a requisição GET
    response = requests.get(f'{ASAAS_URL}?cpfCnpj={cpf_cnpj}', headers=headers)

    # Verificar se a requisição foi bem-sucedida
    if response.status_code == 200:
        return jsonify(response.json())  # Retornar o JSON da resposta
    else:
        return jsonify({"error": "Unable to fetch customer data"}), response.status_code

@paymentJ_bp.route('/customer', methods=['POST'])
def create_customer():
    # Receber os dados enviados no body da requisição
    customer_data = request.get_json()

    headers = retornaHead()

    # Realizar a requisição POST para criar um novo cliente
    response = requests.post(ASAAS_URL, headers=headers, json=customer_data)

    # Verificar se a requisição foi bem-sucedida
    if response.status_code == 200 or response.status_code == 201:
        try:
            return jsonify(response.json())  # Retornar o JSON da resposta
        except requests.exceptions.JSONDecodeError:
            return jsonify({"error": "Response is not in JSON format"}), response.status_code
    else:
        try:
            # Exibir o conteúdo completo da resposta para análise
            print("Erro ao criar cliente: ", response.text)
            # Tentar extrair o JSON de erro
            return jsonify({"error": "Unable to create customer", "details": response.json()}), response.status_code
        except requests.exceptions.JSONDecodeError:
            # Se não for JSON, retornar o texto bruto da resposta
            return jsonify({"error": "Unable to create customer", "details": response.text}), response.status_code

@paymentJ_bp.route('/payment', methods=['POST'])
def create_payment():
    payment_data = request.get_json()  # Dados do pagamento que serão enviados no body da requisição
    customer_id = payment_data.get('customer')

    headers = retornaHead()

    # Verificar se o cliente possui CPF/CNPJ
    customer_url = f'{ASAAS_URL}/{customer_id}'
    customer_response = requests.get(customer_url, headers=headers)

    if customer_response.status_code == 200:
        customer_data = customer_response.json()

        # Verificar se o cliente possui CPF/CNPJ
        if not customer_data.get('cpfCnpj'):
            return jsonify({
                "error": "Customer does not have CPF/CNPJ",
                "details": "CPF/CNPJ is required for credit card payments."
            }), 400

        print(customer_data.get('cpfCnpj'))

        # URL da API do Asaas para criar o pagamento
        payment_url = 'https://sandbox.asaas.com/api/v3/payments'

        # Fazer a requisição POST para criar o pagamento
        response = requests.post(payment_url, headers=headers, json=payment_data)

        # Verificar se a requisição foi bem-sucedida
        if response.status_code == 200 or response.status_code == 201:
            return jsonify(response.json())  # Retorna o JSON da resposta se tudo estiver OK
        else:
            return jsonify({"error": "Unable to create payment", "details": response.text}), response.status_code
    else:
        return jsonify({"error": "Unable to fetch customer data", "details": customer_response.text}), customer_response.status_code

@paymentJ_bp.route('/customer_payment', methods=['POST'])
def customer_payment():
    data = request.get_json()  # Receber os dados enviados no body da requisição
    name = data.get('name')
    cpf_cnpj = data.get('cpfCnpj')
    billing_type = data.get('billingType')
    payment_data = {
        "billingType": billing_type,
        "value": data.get('value'),
        "dueDate": data.get('dueDate')
    }

    headers = retornaHead()

    # Verificar se o cliente já existe
    response = requests.get(f'{ASAAS_URL}?cpfCnpj={cpf_cnpj}', headers=headers)

    if response.status_code == 200 and response.json().get('data'):
        # Cliente encontrado, utilizar o ID retornado
        customer_id = response.json()['data'][0]['id']
    else:
        # Cliente não encontrado, criar um novo com CPF/CNPJ
        customer_data = {
            "name": name,
            "cpfCnpj": cpf_cnpj  # Certifique-se de incluir o CPF/CNPJ
        }
        response = requests.post(ASAAS_URL, headers=headers, json=customer_data)

        if response.status_code == 200 or response.status_code == 201:
            # Cliente criado com sucesso, pegar o ID do novo cliente
            customer_id = response.json().get('id')
        else:
            return jsonify({"error": "Unable to create customer", "details": response.json()}), response.status_code

    # Agora que temos o customer_id, vamos criar o pagamento
    payment_data['customer'] = customer_id
    payment_url = 'https://sandbox.asaas.com/api/v3/payments'

    response = requests.post(payment_url, headers=headers, json=payment_data)

    if response.status_code == 200 or response.status_code == 201:
        # Retornar a URL do pagamento
        payment_url = response.json().get('invoiceUrl')
        return jsonify({"payment_url": payment_url})
    else:
        return jsonify({"error": "Unable to create payment", "details": response.text}), response.status_code


@paymentJ_bp.route('/webhook', methods=['POST'])
def payments_webhook():
    body = request.json

    if body['event'] == 'PAYMENT_CREATED':
        payment = body['payment']
        create_payment(payment)
    elif body['event'] == 'PAYMENT_RECEIVED':
        payment = body['payment']
        receive_payment(payment)
    else:
        print(f"Este evento não é aceito {body['event']}")

    return jsonify({'received': True})

def create_payment(payment):
    # Implementação do create_payment
    print('*********** CREATE PAY *************')
    pass

def receive_payment(payment):
    # Implementação do receive_payment
    print('*********** RECEIVE PAY *************')
    pass

def retornaHead():
    headers = {
        'accept': 'application/json',
        'access_token': ACCESS_TOKEN
    }

    return headers
