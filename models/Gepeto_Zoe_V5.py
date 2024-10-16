import os
from flask import request, jsonify, Blueprint
import requests
import json
import re
from models import legendas
from models.balancesm import distribuir_ordem
from models.formulario_cliente import FormularioCliente
from models.ordens_de_servico import OrdemDeServico
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('OPENAI_API_KEY')

zoe_bp = Blueprint('zoe', __name__)


#TEXTAO = "NOME: Glaucia da Silva Montes Paixao NICHO: Empreendedorismo Feminino  HISTÓRIA: A Soul é um ecossistema para mulheres empreendedoras que queiram empreender sem negligenciar nenhum dos seus papéis como mães e esposas, por exemplo. A Soul tem um tripé de atendimento com agência digital exclusiva para mulheres, uma aceleradora e um braço social."

#BASE = "A partir dos texto abaixo gerar post para midias sociais, devem ser gerados 1 posts com titulo, texto minimo 1000 palavras e 5 hashtags: "

@zoe_bp.route('/', methods=['POST'])
def processar_legendas():
    # CHAMAR os dados a partir do form
    data = request.get_json()
    idForm = data.get('idForm', '')

    # Buscar os dados do formulário pelo ID
    dataForm = FormularioCliente.query.get(idForm)

    # Verificar se o formulário existe
    if not dataForm:
        return jsonify({"message": "Formulário não encontrado"}), 404

    # Converter os dados do formulário para um formato JSON (ajuste de acordo com o seu modelo)
    form_data = {
        'nome_cliente': dataForm.nome_cliente,
        'nicho': dataForm.nicho,
        'nome_negocio': dataForm.nome_negocio,
        'resumo_cliente': dataForm.resumo_cliente,
        'comeco': dataForm.comeco,
        'produto': dataForm.produto,
        'temas': dataForm.temas,
        'whatsapp_cliente': dataForm.whatsapp_cliente
    }
    # Retornar os dados do formulário como resposta JSON
    # return jsonify(form_data), 200

    textao = 'Nome: ' + dataForm.nome_cliente + ' Nicho: ' + dataForm.nicho + ' Nome do Negócio: ' + dataForm.nome_negocio
    textao = textao + ' Cliente ideial: ' + dataForm.resumo_cliente + ' História: ' + dataForm.comeco + ' Produto: ' + dataForm.produto + ' Temas: ' + dataForm.temas

    return processar_legendas_geral(dataForm.whatsapp_cliente, textao, idForm)


def processar_legendas_geral(whatsCliente, textao, form_id):
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

        #Coloca um SM para tratar
        ordemSM = distribuir_ordem(form_id)
        POSTS: int = 0

        # URL correta para a API de chat completions
        response = requests.post("https://api.openai.com/v1/chat/completions",
                                 headers=headers, data=json.dumps(data))

        if response.status_code == 200 or response.status_code == 201:
            output = response.json().get('choices', [{}])[0].get('message', {}).get('content', '')
            print(output)
            # Regex para identificar os blocos de texto que começam com ### Headline e terminam com ### Hashtags
            pattern = r'### Headline\n+([^\n]+)\n+### Legenda\n+([^\n]+)\n+([\s\S]+?)\n+### Hashtags\n+([^\n]+)'

            # Extrai todos os blocos correspondentes
            blocks = re.findall(pattern, output)

            # Contagem de blocos
            block_count = len(blocks)
            print("********** TEMOS: " + str(block_count) + " Blocos de Legenda")
            exit()
            i = 0

            for i, block in enumerate(blocks[:30], start=1):
                headline, legenda, conteudo, hashtags = block
                print(f"Bloco {i}:")
                print(f"### Headline\n{headline}")
                print(f"### Legenda\n{legenda}")
                print(f"{conteudo}")
                print(f"### Hashtags\n{hashtags}\n")

                POSTS = POSTS + block_count
                print('***************** BLOCKS ***************************')
                print(POSTS)
                print('******************BLOCKS **************************')
                # Extraindo a Headline (tanto com *** ou ###)
                headline_match = re.search(r'(?:\*\*\*|###)?\s*Headline\s*\n(.*)', output)
                headline = headline_match.group(1).strip() if headline_match else 'Headline não encontrada'

                # Extraindo a Legenda (tanto com ou sem *** ou ###)
                legenda_match = re.search(r'(?:\*\*\*|###)?\s*Legenda\s*\n([\s\S]*?)(#|$)', output)
                legenda = legenda_match.group(1).strip() if legenda_match else output  # 'Legenda não encontrada'

                # Extraindo as hashtags
                hashtags = ' '.join(re.findall(r'#\w+', output))

                # Exibindo os resultados
                print("Headline:", headline)
                print("Legenda:", legenda)
                print("Hashtags:", hashtags)

                legenda_data = {
                    "id_form": form_id,  # ID fixo vindo de outra fonte
                    "dia_post":  i + 1,
                    "ds_legenda": legenda,
                    "img_legenda": '',  #ur_limg,
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

        print('BORA AVISAR CLIENTE: ....')
        print("ENVIAR MENSAGEM NO WHATS.....")
        URLTigor = "https://tigor.itlabs.app/wpp/api"
        payload = {
            "app": "3bd82d2e-3077-4226-a366-1338eb3ed589",
            "number": whatsCliente,
            "message": "Parabens! Seus posts estão em produção.\n Obrigado por escolher a 30 Posts. \n Quando estirem prontos lhe avisaremos para entrar na plataforma e verificar seus posts.",
            "type": "text",
            "url": ""
        }

        headers = {
            "Content-Type": "application/json"  # Define que o conteúdo enviado é JSON
        }

        responseWhats = requests.post(URLTigor, json=payload, headers=headers)

        if responseWhats.status_code == 200 or responseWhats.status_code == 201:
            print('Cliente informado com sucesso!')
        else:
            print('Erro ao informar cliente:')
            print(responseWhats.text)

        return jsonify({"message": "Legendas processadas e enviadas com sucesso."}), 201

    except Exception as e:
        return jsonify({"error": "Erro ao processar legendas", "details": str(e)}), 500
