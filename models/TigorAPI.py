import requests

class TigorAPI:
    def __init__(self, number, message, type="text", url=""):
        self.URLTigor = "https://tigor.itlabs.app/wpp/api"
        self.payload = {
            "app": "3bd82d2e-3077-4226-a366-1338eb3ed589",
            "number": number,
            "message": message,
            "type": type,
            "url": url
        }

    def send_message(self):
        headers = {
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(self.URLTigor, json=self.payload, headers=headers)
            if response.status_code == 200 or response.status_code == 201:
                print("Mensagem enviada com sucesso!")
                return response.json()  # Retorna a resposta da API em JSON
            else:
                print(f"Erro ao enviar a mensagem. Status: {response.status_code}")
                print("Detalhes:", response.text)
                return None
        except Exception as e:
            print(f"Erro ao enviar a mensagem: {str(e)}")
            return None


