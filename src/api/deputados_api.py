import requests

class deputadoAPI:
    def __init__ (self, base_url: str):
        self.base_url = "https://dadosabertos.camara.leg.br/api/v2/"
        self.headers = {
            "Accept": "application/json"
        }

    def get_dados(self, endpoint: str, params: dict = None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code == 200: # esse 200 é o "ok"
            return response.json() #retorna a resposta
        else:
            raise Exception(f'Erro {response.status_code}: {response.text}') # caso dê erro para verificarmos o que aconteceu
        
        