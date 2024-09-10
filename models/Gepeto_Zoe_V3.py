from flask import request, jsonify, Blueprint, make_response
import requests
import json

from models import legendas

# Defina sua chave da API da OpenAI
API_KEY = "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"

zoe_bp = Blueprint('zoe', __name__)


#TEXTAO = "NOME: Glaucia da Silva Montes Paixao NICHO: Empreendedorismo Feminino  HISTÓRIA: A Soul é um ecossistema para mulheres empreendedoras que queiram empreender sem negligenciar nenhum dos seus papéis como mães e esposas, por exemplo. A Soul tem um tripé de atendimento com agência digital exclusiva para mulheres, uma aceleradora e um braço social."

#BASE = "A partir dos texto abaixo gerar post para midias sociais, devem ser gerados 1 posts com titulo, texto minimo 1000 palavras e 5 hashtags: "

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
            #"id": "asst_XlQl4tqzHEnlYOC49tkxRgBX",
            "model": "gpt-4o-2024-05-13",  # Atualize o modelo se necessário
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                #{"role": "user", "content": "Estou usando a Zoe?"}
                {"role": "user", "content": BASE + textao}
            ],
            "temperature": 0.7
            #"max_tokens": 50
        }

        # URL correta para a API de chat completions
        response = requests.post("https://api.openai.com/v1/chat/completions",
                                 headers=headers, data=json.dumps(data))

        # Verifique o código de status da resposta
        if response.status_code == 200:
            try:
                # Tente acessar a resposta de chat
                output = response.json()['choices'][0]['message']['content']
                print(output)
            except KeyError:
                # Imprima a resposta completa se 'choices' não estiver presente
                print("Erro: 'choices' não encontrado na resposta.")
                print(response.json())
        else:
            print(f"Erro: A requisição falhou com o código de status {response.status_code}")
            print(response.text)

        if response.status_code == 200:
            output = response.json().get('choices', [{}])[0].get('message', {}).get('content', '')
            print(output)

            legenda_data = {
                "id_form": '1',
                "dia_post": 30,
                "ds_legenda": 'output',
                "bl_aprovado": False,
                "bl_revisar": False,
                "ds_revisao": None
            }

            # Tentar enviar a legenda usando o serviço de legendas
            legenda_response = requests.post(
                "http://127.0.0.1:5000/legendas/",
                json=legenda_data
            )

            if legenda_response.status_code == 201:
                return jsonify({"message": "Legenda processada e enviada com sucesso."}), 201
            else:
                return jsonify({"error": "Erro ao enviar legenda", "details": legenda_response.text}), 500
        else:
            return jsonify({"error": "Erro na resposta da API OpenAI", "details": response.text}), 500

    except Exception as e:
        return jsonify({"error": "Erro ao processar legendas", "details": str(e)}), 500

