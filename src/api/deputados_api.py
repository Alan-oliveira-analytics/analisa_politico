import requests

class deputadoAPI:

    """
    Classe para realizar requisições GET a uma API com base em uma URL e, opcionalmente, um token de autenticação caso necessário.

    """

    def __init__ (self, base_url: str, token: str = None):

        """
        Inicializa com a URL base da API e, se necessário, um token de autenticação.
    
        Parâmetros:
        base_url (str): URL base da API
        token (str, opcional): token de autenticação no formato Bearer

        """

        self.base_url = "https://dadosabertos.camara.leg.br/api/v2/"
        self.headers = {
            "Accept": "application/json"
        }
        if token: # se não for None
            self.headers['Authorization'] = f'Bearer {token}'


    def get_dados(self, endpoint: str, params: dict = None):

        """
        Faz uma requisição GET ao endpoint fornecido e retorna os dados da resposta em formato JSON

        Parâmetros:
        endpoint (str): caminho do recurso desejado 
        params (dict, opcional): Parâmetros da requisição (query string)

        Retorna:
        dict: Resposta da API em formato JSON

        Exceções:
        Lança exception se o status da resposta não for 200

        """
        
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code == 200: # esse 200 é o "ok"
            return response.json() #retorna a resposta
        else:
            raise Exception(f'Erro {response.status_code}: {response.text}') # caso dê erro para verificarmos o que aconteceu
        
        