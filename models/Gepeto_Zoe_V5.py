from flask import request, jsonify, Blueprint, make_response
import requests
import json
import re

from sqlalchemy import false

from models import legendas
from models.Zoe_Img import gerar_imagem

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

    return processar_legendas(textao)


def processar_legendas(textao, form_id=0):
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
            "model": "gpt-4o-2024-05-13",  # Atualize o modelo se necessário
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": BASE + textao}
            ],
            "temperature": 0.7
        }

        for i in range(31):
            # Coloque aqui o código que deseja executar 30 vezes
            print(f"Execução número {i + 1}")

            # URL correta para a API de chat completions
            response = requests.post("https://api.openai.com/v1/chat/completions",
                                    headers=headers, data=json.dumps(data))

            if response.status_code == 200:
                output = response.json().get('choices', [{}])[0].get('message', {}).get('content', '')
                #print(output)

                # Extraindo a Headline (tanto com *** ou ###)
                headline_match = re.search(r'(?:\*\*\*|###) Headline\n(.*)', output)
                headline = headline_match.group(1) if headline_match else 'Headline não encontrada'

                # Extraindo a Legenda (tanto com *** ou ###)
                legenda_match = re.search(r'(?:\*\*\*|###) Legenda\n([\s\S]*?)(#|$)', output)
                legenda = legenda_match.group(1).strip() if legenda_match else 'Legenda não encontrada'

                # Extraindo as hashtags
                hashtags = ' '.join(re.findall(r'#\w+', output))

                # Exibindo os resultados
                print("Headline:", headline)
                print("Legenda:", legenda)
                print("Hashtags:", hashtags)

                legenda_data = {
                    "id_form": form_id,  # ID fixo vindo de outra fonte
                    "dia_post": i,
                    "ds_legenda": legenda,
                    "img_legenda": '', #ur_limg,
                    "bl_aprovado": False,
                    "bl_revisar": False,
                    "ds_revisao": '',
                    "bl_planner": False,
                    "ds_headline": headline,
                    "ds_hashtags": hashtags
                }

                print('ENVIANDO LEGENDAS....')

                # Enviando a legenda usando o serviço de legendas
                legenda_response = legendas.geraLegenda(legenda_data)

                #VERIFICAR VALIDACAO RETORNO
                #if legenda_response.status_code == 201:
                #    print(f"Legenda para o dia {1} enviada com sucesso.")
                #else:
                #    print(f"Erro ao enviar legenda para o dia {1}: {legenda_response.text}")

        return jsonify({"message": "Legendas processadas e enviadas com sucesso."}), 201

    except Exception as e:
        return jsonify({"error": "Erro ao processar legendas", "details": str(e)}), 500
