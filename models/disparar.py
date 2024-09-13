import requests
from flask import Flask, request, jsonify, Blueprint

from models import Gepeto_Zoe_V5
from models.clientes import consultaTele
from utils.token_verify import token_required

disparar_bp = Blueprint('disparar', __name__)


@disparar_bp.route('/', methods=['POST'])
@token_required
def disparar_chamadas(token_data):
    form_id = token_data.get('id')
    print(form_id)
    user_id = token_data.get('user_id')
    print(user_id)
    data = request.get_json()

    # Verifica se o JSON contém uma lista de informações
    if not data or not isinstance(data, list):
        return jsonify({"error": "O corpo da solicitação deve ser uma lista de objetos JSON."}), 400

    results = []

    # Itera sobre cada item da lista
    for item in data:
        try:
            # Acessa os valores de cada objeto dentro da lista
            nome_cliente = item.get('nome_cliente', '')
            whatsapp_cliente = item.get('whatsapp_cliente', '')
            email_cliente = item.get('email_cliente', '')
            nome_negocio = item.get('nome_negocio', '')
            nicho = item.get('nicho', '')
            resumo_cliente = item.get('resumo_cliente', '')
            comeco = item.get('comeco', '')
            temas = item.get('temas', '')
            produto = item.get('produto', '')
            identidade_visual_1 = item.get('identidade_visual_1', '')
            identidade_visual_2 = item.get('identidade_visual_2', '')
            estilo = item.get('estilo', '')
            whatsapp_negocio = item.get('whatsapp_negocio', '')
            site = item.get('site', '')

            # Formata os dados em uma string ou executa outra lógica com esses dados
            texto = (
                f"NOME: {nome_cliente} \n"
                f"NOME DO NEGÓCIO: {nome_negocio} \n"
                f"NICHO: {nicho} \n"
                f"RESUMO: {resumo_cliente} \n"
                f"COMEÇO: {comeco} \n"
                f"TEMAS: {temas} \n"
                f"PRODUTO: {produto} \n"
                f"ESTILO: {estilo} \n"

            )

            # Dispara a chamada para o serviço /zoe com os dados de cada item
            response = (Gepeto_Zoe_V5.processar_legendas(texto, form_id))


        except Exception as e:
            # Captura erros durante a chamada e adiciona à lista de resultados
            results.append({
                "item": item,
                "status_code": "error",
                "error": str(e)
            })

    # Retorna os resultados de todas as chamadas feitas
    return jsonify(results), 200
