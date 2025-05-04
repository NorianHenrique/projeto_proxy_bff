
from dotenv import load_dotenv, find_dotenv
import os

# localiza o arquivo de .env
dotenv_file = find_dotenv()
# Carrega o arquivo .env
load_dotenv(dotenv_file)

# Valores obtidos de variáveis de ambiente ou hardcoded como fallback
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

PROXY_PORT = os.getenv("PROXY_PORT", 5000)
PROXY_DEBUG = os.getenv("PROXY_DEBUG", False)

API_SSL_VERIFY = True if os.getenv('API_SSL_VERIFY', True).lower() == 'true' else False

API_URL = os.getenv('API_URL', 'https://127.0.0.1:4443')
API_USERNAME_TOKEN = os.getenv('API_USERNAME_TOKEN', 'abc')
API_PASSWORD_TOKEN = os.getenv('API_PASSWORD_TOKEN', 'bolinhas')

API_ENDPOINT_TOKEN = os.getenv('API_ENDPOINT_TOKEN', f'{API_URL}/token/')
API_ENDPOINT_FUNCIONARIO = os.getenv('API_ENDPOINT_FUNCIONARIO', f'{API_URL}/funcionario/')
API_ENDPOINT_CLIENTE = os.getenv('API_ENDPOINT_CLIENTE', f'{API_URL}/cliente/')
API_ENDPOINT_PRODUTO = os.getenv('API_ENDPOINT_PRODUTO', f'{API_URL}/produto/')

TEMPO_SESSION = os.getenv('TEMPO_SESSION',60)