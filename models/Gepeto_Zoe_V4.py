import re
import requests
from flask import request, jsonify, Blueprint

zoe_bp = Blueprint('zoe', __name__)

API_KEY = "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"

@zoe_bp.route('/', methods=['POST'])
def processar_legendas():
    data = request.get_json()
    textao = data.get('textao', '')

    if not textao:
        return jsonify({"error": "Texto de entrada não fornecido."}), 400

    try:
        with open('./models/promptBase.txt', 'r', encoding='utf8') as arquivo:
            BASE = arquivo.read()

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
            "OpenAI-Beta": "assistants=v2",
            "id": "asst_XlQl4tqzHEnlYOC49tkxRgBX"
        }

        data = {
            "model": "gpt-4o-2024-05-13",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": BASE + textao}
            ],
            "temperature": 0.7
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)

        if response.status_code == 200:
            output = response.json().get('choices', [{}])[0].get('message', {}).get('content', '')
            print(output)

            # Dividindo o output em partes baseadas no padrão "**Número"
            partes = re.split(r'\*\*(\d+)', output)


            # Iterando sobre as partes e enviando cada legenda separadamente
            for i in range(1, len(partes), 2):
                dia_post = int(partes[i])  # Número após "**"
                texto_legenda = partes[i + 1].strip()  # Texto da legenda

                legenda_data = {
                    "id_form": '1',  # ID fixo vindo de outra fonte
                    "dia_post": dia_post,
                    "ds_legenda": texto_legenda,
                    "bl_aprovado": False,
                    "bl_revisar": False,
                    "ds_revisao": None
                }

                # Enviando a legenda usando o serviço de legendas
                legenda_response = requests.post(
                    "http://127.0.0.1:5000/legendas/",
                    json=legenda_data
                )

                if legenda_response.status_code == 201:
                    print(f"Legenda para o dia {dia_post} enviada com sucesso.")
                else:
                    print(f"Erro ao enviar legenda para o dia {dia_post}: {legenda_response.text}")

            return jsonify({"message": "Legendas processadas e enviadas com sucesso."}), 201

        else:
            return jsonify({"error": "Erro na resposta da API OpenAI", "details": response.text}), 500

    except Exception as e:
        return jsonify({"error": "Erro ao processar legendas", "details": str(e)}), 500
