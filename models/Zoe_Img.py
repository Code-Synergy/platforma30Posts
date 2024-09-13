import re
import os
import random
import string

import requests
from supabase import create_client, Client


API_KEY = "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"

# URL e Key do Supabase
SUPABASE_URL = "https://urxsxcaesrhgtwwvxmku.supabase.co"
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVyeHN4Y2Flc3JoZ3R3d3Z4bWt1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjIyNjEwNTcsImV4cCI6MjAzNzgzNzA1N30.fxFHVZ7ifIvBrkKGNZFcZjlRdH8FiJ9Hrlbq3SUYi-I"
BUCKET_NAME = "30Posts"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)

def gerar_imagem(texto):
    print('GERANDO IMAGEM...')

    # Extrair hashtags usando expressão regular
    hashtags = re.findall(r'#\w+', texto)

    # Juntar as hashtags em uma string separada por espaço ou vírgula, conforme necessário
    hashtags_extraidas = ' '.join(hashtags)
    hashtags_extraidas = hashtags_extraidas.replace("#", ",")
    print('**************************************************')
    print(hashtags_extraidas)
    print('**************************************************')
    """
    Gera uma imagem com base no texto usando a API da OpenAI.
    """

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",  # Certifique-se de que a API Key tem acesso à geração de imagens
    }

    #Monta o prompt
    prompt = 'Crie uma cena inspirada em ' + hashtags_extraidas + 'A cena deve capturar o espírito desses temas de forma visual e abstrata, sem incluir letras, palavras ou qualquer forma de texto A imagem deve ser harmoniosa, criativa e focada nos conceitos das hashtags, sem a presença de palavras ou qualquer forma de escrita.'

    # Parâmetros da geração de imagem
    data_img = {
        "prompt": prompt,  # Texto usado para gerar a imagem
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
            #return caminho_arquivo
        else:
            print(f"Erro ao baixar a imagem: {response2.status_code}")
            #return None

        # Fazer upload da imagem para o Supabase Storage
        supabase_response = upload_to_supabase(caminho_arquivo, nomeArqImg)

        if supabase_response:
            print(f"Imagem salva no Supabase: {supabase_response}")

            #file.close()
            #os.remove(caminho_arquivo)
        else:
            print("Erro ao fazer upload para o Supabase.")

        return supabase_response

    else:
        # Exibe a resposta completa para identificar o erro
        print(f"Erro ao gerar imagem: {response_img.text}")
        return None  # Retorna None para evitar erros adicionais


def upload_to_supabase(filepath, filename):
    """
    Faz upload da imagem para o Supabase Storage.
    """
    # URL para upload no Supabase Storage
    upload_url = f"{SUPABASE_URL}/storage/v1/object/{BUCKET_NAME}/{filename}"
    print('MANDA PARA SUPABASE')

    # Faz o upload do arquivo para o bucket especificado
    #response = supabase.storage.from_(BUCKET_NAME).upload('Eu_Terno2.png', "C:\\Users\\jdrpi\\OneDrive\\Imagens\\Eu_Terno2.png")
    response = supabase.storage.from_(BUCKET_NAME).upload(filename,filepath)

    if response.status_code == 200 or response.status_code == 201:
        # URL completa para acesso ao arquivo no Supabase
        return f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{filename}"
    else:
        print(f"Erro ao fazer upload para o Supabase: {response.text}")
        return None
