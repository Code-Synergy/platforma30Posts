import re

import requests

API_KEY = "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"


def gerar_imagem(texto):
    print('ENTROU PARA GERAR IMAGEM')
    print(texto)

    # Extrair hashtags usando expressão regular
    hashtags = re.findall(r'#\w+', texto)

    # Juntar as hashtags em uma string separada por espaço ou vírgula, conforme necessário
    hashtags_extraidas = ' '.join(hashtags)
    hashtags_extraidas = hashtags_extraidas.replace("#", ",")
    print('**************************************************')
    print('**************************************************')
    print(hashtags_extraidas)
    print('**************************************************')
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
        return image_url
    else:
        # Exibe a resposta completa para identificar o erro
        print(f"Erro ao gerar imagem: {response_img.text}")
        return None  # Retorna None para evitar erros adicionais
