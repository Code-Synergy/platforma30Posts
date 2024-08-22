import requests
import json

# Defina sua chave da API da OpenAI
API_KEY = "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"

# Texto que você quer enviar para o assistente
TEXTAO = "NOME: Jean Daniel Rosa Pires NICHO: Desenvolvimento de software, consultoria em transformação digital, soluções em automação HISTÓRIA: Minha paixão pela inovação e tecnologia sempre esteve presente na minha vida. A capacidade das tecnologias de mudar o mundo ao nosso redor sempre me fascinou. A motivação para fundar a Code Synergy foi minha curiosidade e entusiasmo. Tudo começou com um objetivo claro: ajudar as empresas a prosperarem na era digital. Aprendi que muitas empresas não conseguiram acompanhar o ritmo acelerado das inovações tecnológicas, perdendo oportunidades valiosas de crescimento e melhoria. Eu desejava mudar isso e ajudar na transformação. Nossa missão aqui na Code Synergy é criar soluções tecnológicas que não apenas resolvam problemas, mas também abram novas possibilidades. Nosso objetivo é entender profundamente os requisitos de nossos clientes e fornecer soluções personalizadas que são realmente diferenciadoras. Buscamos sempre oferecer excelência e inovação, seja por meio do desenvolvimento de software, automação de processos ou consultoria em transformação digital. Observar como nossas soluções beneficiam os negócios de nossos clientes me motiva todos os dias. É gratificante saber que estamos ajudando as empresas a crescer, aumentar a eficiência e alcançar seus objetivos com mais eficiência. Essa é a verdade por trás do trabalho que realizamos na Code Synergy. Compartilhar essa jornada com nossa audiência é uma maneira de demonstrar que um verdadeiro compromisso com a excelência e uma paixão genuína pela inovação estão por trás de todas as tecnologias que estamos oferecendo. Além disso, é essa paixão que nos motiva a continuar crescendo e oferecendo o melhor para nossos clientes."

BASE = "A partir dos texto abaixo gerar post para midias sociais, devem ser gerados 3 posts com titulo, texto minimo 250 palavras e 5 hashtags: "

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}",
    "OpenAI-Beta": "assistants=v2"
}

data = {
    "model": "gpt-4",  # Use o modelo que você deseja
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": BASE + TEXTAO}
    ],
    "temperature": 0.7,
    #"max_tokens": 500  # Aumente conforme necessário para capturar todas as respostas
}

# URL correta para a API de chat completions
response = requests.post("https://api.openai.com/v1/chat/completions",
                         headers=headers, data=json.dumps(data))

# Verifique a resposta
if response.status_code == 200:
    try:
        # Processa e imprime a resposta do assistente
        output = response.json()['choices'][0]['message']['content']
        print("Resposta do assistente:", output)
    except KeyError:
        print("Erro: 'choices' não encontrado na resposta.")
        print(response.json())
else:
    print(f"Erro: A requisição falhou com o código de status {response.status_code}")
    print(response.text)
