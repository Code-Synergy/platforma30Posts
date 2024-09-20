import requests

# Sua API Key da DeepAI
api_key = '47818b0b-0f71-4161-8180-0e7d40e3afa3'

# Texto que descreve a imagem que você deseja gerar
prompt = 'Um retrato em close-up de um CTO em um ambiente de escritório moderno, olhando pensativo para um monitor com gráficos e códigos. A imagem deve transmitir seriedade e foco, destacando a importância e a responsabilidade da posição.'

# Enviar a requisição para a API de geração de imagens (text2img)
response = requests.post(
    "https://api.deepai.org/api/text2img",
    data={'text': prompt},
    headers={'api-key': api_key}
)

# Verificar a resposta e pegar o link da imagem gerada
if response.status_code == 200:
    output_url = response.json()['output_url']
    print(f"Imagem gerada: {output_url}")
else:
    print(f"Erro: {response.status_code}, {response.text}")
