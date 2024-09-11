from flask import request, jsonify, Blueprint, make_response
import requests
import json
import re

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

        if response.status_code == 200:
            output = response.json().get('choices', [{}])[0].get('message', {}).get('content', '')
            print(output)

            # Verifica qual padrão está presente no output e divide o texto conforme o padrão encontrado
            #if '###' in output:
            #    partes = re.split(r'###\s*(\d+)', output)  # Padrão "### Número"
            #elif '**' in output:
            #    partes = re.split(r'\*\*(\d+)', output)  # Padrão "**Número"
            #else:
            #    return jsonify({"error": "Nenhum padrão reconhecido encontrado no texto."}), 400

            ## Iterando sobre as partes e enviando cada legenda separadamente
            #for i in range(1, len(partes), 2):
            #    print('*************************************************************************')
            #    dia_post = int(partes[i])  # Número após "###"
            #    print(dia_post)
            #    texto_legenda = partes[i + 1].strip()  # Texto da legenda
            #    print(texto_legenda)

            #    legenda_data = {
            #        "id_form": '1',  # ID fixo vindo de outra fonte
            #        "dia_post": dia_post,
            #        "ds_legenda": texto_legenda,
            #        "bl_aprovado": False,
            #        "ds_revisao": None
            #    }
            #    print('*************************************************************************')
            #    print('*************************************************************************')

            #GERAR IMAGEM

            data_img = {
                "prompt": output,
                "n": 1,
                "size": "1024x1024"
            }

            response_img = requests.post("https://api.openai.com/v1/images/generations", headers=headers, json=data_img)
            if response_img.status_code == 200:
                image_url = response_img.json()['data'][0]['url']
            else:
                print(f"Erro ao gerar imagem: {response.text}")
                return None

            print(image_url)

            legenda_data = {
                "id_form": '1',  # ID fixo vindo de outra fonte
                "dia_post": 1,
                "ds_legenda": output,
                "bl_aprovado": False,
                "ds_revisao": None
            }


            # Enviando a legenda usando o serviço de legendas
            legenda_response = requests.post(
                "http://127.0.0.1:5000/legendas/",
                json=legenda_data
            )

            if legenda_response.status_code == 201:
                print(f"Legenda para o dia {1} enviada com sucesso.")
            else:
                print(f"Erro ao enviar legenda para o dia {1}: {legenda_response.text}")

        return jsonify({"message": "Legendas processadas e enviadas com sucesso."}), 201

    except Exception as e:
        return jsonify({"error": "Erro ao processar legendas", "details": str(e)}), 500
