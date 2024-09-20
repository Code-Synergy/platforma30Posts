import requests

def generate_image():
    API_KEY = "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"
    prompt = "Com base no perfil do instagram @codesynergytech, gere uma imagem no formato feed quadrado (1080x1080) que mais se encaixa no nicho e no estilo do usuário. Quero uma cena compatível com conteúdo criado. De preferência para retrato em close-up, tomada autêntica, que transmite a emoção do texto gerado."
    url = 'https://api.openai.com/v1/images/generations'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024"
    }

    response = requests.post(url, headers=headers, json=data)
    print(response.status_code)

    if response.status_code == 200:
        img_data =response.json()['data'][0]['url']
        print(img_data)
        with open(img_data, 'wb') as handler:
            handler.write(img_data)
        return response.json()['data'][0]['url']  # Link para o arquivo gerado
    else:
        return None

generate_image()
