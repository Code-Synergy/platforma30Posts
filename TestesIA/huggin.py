import requests

# Sua API Key do Hugging Face
api_key = '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'

# Texto que descreve a imagem que você deseja gerar
prompt = 'Um retrato em close-up de um CTO em um ambiente de escritório moderno, olhando pensativo para um monitor com gráficos e códigos. A imagem deve transmitir seriedade e foco, destacando a importância e a responsabilidade da posição.'

# URL do modelo Stable Diffusion no Hugging Face
api_url = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"

# Cabeçalhos da requisição (incluindo a API Key)
headers = {
    "Authorization": f"Bearer {api_key}"
}

# Dados da requisição (prompt de texto)
data = {
    "inputs": prompt
}

# Enviar a requisição para a API
response = requests.post(api_url, headers=headers, json=data)

# Verificar a resposta e salvar a imagem gerada
if response.status_code == 200:
    # A resposta é a imagem em formato binário
    with open("imagem_gerada.png", "wb") as f:
        f.write(response.content)
    print("Imagem gerada e salva como 'imagem_gerada.png'")
else:
    print(f"Erro: {response.status_code}, {response.text}")
