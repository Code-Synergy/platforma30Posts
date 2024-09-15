import os
import random
import re
import string

from flask import request, jsonify, Blueprint, make_response
import requests
import json

from models import legendas
from models.Zoe_Img import gerar_imagem, upload_to_supabase

# Defina sua chave da API da OpenAI
API_KEY = "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"

zoeFluxo1_bp = Blueprint('zoeFluxo1', __name__)

@zoeFluxo1_bp.route('/', methods=['POST'])
def processar_fluxo1():

    #form_id = token_data.get('id')
    form_id = 0

    data = request.get_json()

    if not data:
        return jsonify({"error": "Texto de entrada não fornecido."}), 400

    return processar_legendas(data, form_id)


def processar_legendas(data, form_id=0):
    print('**************************************')
    print('PROCESSANDO LEGENDAS DO FORM:' + str(form_id))
    print('**************************************')

    nomenegocio = data.get("nomenegocio")
    socialmedia = data.get("socialmedia")
    objetivo = data.get("objetivo")
    telefone = data.get("telefone")

    try:
        with open('./models/promptFluxo1.txt', 'r', encoding='utf8') as arquivo:
            fluxo1 = arquivo.read()
            fluxo1 = fluxo1.replace('[bazinga1]', nomenegocio)
            fluxo1 = fluxo1.replace('[bazinga2]', socialmedia)
            fluxo1 = fluxo1.replace('[bazinga3]', objetivo)

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
                {"role": "user", "content": fluxo1}
            ],
            "temperature": 0.7
            #"max_tokens": 50
        }

        # URL correta para a API de chat completions
        response = requests.post("https://api.openai.com/v1/chat/completions",
                                 headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            print(response)
            output = response.json().get('choices', [{}])[0].get('message', {}).get('content', '')
            print(output)

            match = re.search(r'Headline:(.*?)Legenda:', output, re.DOTALL)
            # Verificando se o padrão foi encontrado e extraindo o texto
            if match:
                texto_headline = match.group(1).strip()

                # Exibindo o texto encontrado
                print("Texto entre Headline e Legenda:\n")
                print(texto_headline)
            else:
                print("Não foi possível encontrar o trecho entre 'Headline' e 'Legenda'.")

            # Usando regex para capturar o texto entre "Legenda" e "Imagem"
            match_legenda_imagem = re.search(r'Legenda:(.*?)Imagem:', output, re.DOTALL)

            # Usando regex para capturar o texto após "Imagem"
            match_imagem_final = re.search(r'Imagem:(.*)', output, re.DOTALL)

            # Verificando se os padrões foram encontrados e extraindo os textos
            texto_legenda = match_legenda_imagem.group(
                1).strip() if match_legenda_imagem else "Não foi possível encontrar o trecho entre 'Legenda' e 'Imagem'."
            texto_imagem = match_imagem_final.group(
                1).strip() if match_imagem_final else "Não foi possível encontrar o trecho após 'Imagem'."

            print(texto_legenda)
            print('**********************************************************')
            print(texto_imagem)

            #prompt_imagem = 'Com base no perfil do instagram ' + socialmedia + ', gere uma imagem no formato feed quadrado (1080x1080) que mais se encaixa no nicho e no estilo do usuário. Quero uma cena compatível com conteúdo criado. De preferência para retrato em close-up, tomada autêntica, que transmite a emoção do texto gerado.'

            print('GERANDO IMAGEM...')

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_KEY}",
                "OpenAI-Beta": "assistants=v2",
                "id": "asst_XlQl4tqzHEnlYOC49tkxRgBX"
            }
            # Parâmetros da geração de imagem
            data_img = {
                "prompt": texto_imagem,  # Texto usado para gerar a imagem
                "n": 1,  # Número de imagens a serem geradas
                "size": "1024x1024"  # Tamanho da imagem gerada
            }

            # URL correta para a API de geração de imagens
            response_img = requests.post("https://api.openai.com/v1/images/generations", headers=headers, json=data_img)


            if response_img.status_code == 200:
                image_url = response_img.json()['data'][0]['url']
                print(image_url)
                # Fazer download da imagem gerada
                response2 = requests.get(image_url)
                # Verifica se o download foi bem-sucedido
                if response2.status_code == 200:
                    # Caminho onde o arquivo será salvo (na raiz do projeto)
                    nomeArqImg = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + ".png"
                    print(nomeArqImg)
                    caminho_arquivo = os.path.join(os.getcwd(), nomeArqImg)

                    # Salva a imagem na raiz do projeto
                    with open(caminho_arquivo, "wb") as file:
                        file.write(response2.content)

                    print(f"Imagem salva com sucesso em: {caminho_arquivo}")
                    print('****************************************')
                    print(caminho_arquivo)
                    print('*****************************************')
                    # Fazer upload da imagem para o Supabase Storage
                    supabase_response = upload_to_supabase(caminho_arquivo, nomeArqImg)
                    if supabase_response:
                        print(f"Imagem salva no Supabase: {supabase_response}")
                        legenda_data = {
                            "id_form": form_id,
                            "dia_post": 1,
                            "ds_legenda": output,
                            "img_legenda": supabase_response,
                            "bl_aprovado": True,
                            "ds_revisao": ''
                        }

                        print('ENVIANDO LEGENDAS....')
                        # Enviando a legenda usando o serviço de legendas
                        legenda_response = legendas.geraLegenda(legenda_data)
                        print('ENVIADAS AS LEGENDAS!!!')
                        print('ESTA AQUI SEU POST: ' + output)

                        URLTigor = "https://tigor.itlabs.app/wpp/api"
                        #payload = {
                        #    "app": "3bd82d2e-3077-4226-a366-1338eb3ed589",
                        #    "number": telefone,
                        #    "message": "Parabens! Seu post chegou! \n " + output,
                        #    "type": "text",
                        #    "url": ""
                        #}

                        #headers = {
                        #    "Content-Type": "application/json"  # Define que o conteúdo enviado é JSON
                        #}

                        #responseWhats = requests.post(URLTigor, json=payload, headers=headers)

                        #if responseWhats.status_code == 200 or responseWhats.status_code == 201:
                        #    print('POST enviado ao cliente com com sucesso!')
                        #else:
                        #    print('Erro ao enviar post ao cliente:')
                        #    print(responseWhats.text)

                        payload_img = {
                            "app": "3bd82d2e-3077-4226-a366-1338eb3ed589",
                            "number": telefone,
                            "message": "Seu post chegou ! \n " + texto_headline + " \n" + texto_legenda,
                            "type": "image",
                            "url": image_url
                        }

                        headers = {
                            "Content-Type": "application/json"  # Define que o conteúdo enviado é JSON
                        }

                        responseWhats = requests.post(URLTigor, json=payload_img, headers=headers)

                        if responseWhats.status_code == 200 or responseWhats.status_code == 201:
                            print('IMAGEM enviada ao cliente com com sucesso!')
                            print(f"Legenda para o dia {1} enviada com sucesso.")
                            file.close()
                            os.remove(caminho_arquivo)

                        else:
                            print('Erro ao enviar IMAGEM ao cliente:')
                            print(responseWhats.text)
                            print(f"Erro ao enviar legenda para o dia {1}: {legenda_response.text}")
                            file.close()
                            os.remove(caminho_arquivo)
                    else:
                        print("Erro ao fazer upload para o Supabase.")
                    return supabase_response
                else:
                    print(f"Erro ao baixar a imagem: {response2.status_code}")
                    # return None
            else:
                return jsonify({"error": "Erro ao processar legendas", "details": str(response_img.text)}), 500
        return jsonify({"message": "Legendas processadas e enviadas com sucesso."}), 201
    except Exception as e:
        return jsonify({"error": "Erro ao processar legendas", "details": str(e)}), 500
