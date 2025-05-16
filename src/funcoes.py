from flask import session
from datetime import datetime, timedelta
import requests
from settings import API_ENDPOINT_TOKEN, API_USERNAME_TOKEN, API_PASSWORD_TOKEN, API_SSL_VERIFY
import logging

class Funcoes(object):
# função para obter o token da API externa, retorna o json do token obtido ou do erro - os dados do token são armazenados na sessão do Flask para uso posterior
    @staticmethod
    def get_api_token():
        try:
            # Limpa a sessão anterior
            session.clear()
            logging.info(f"Requisitando novo token de {API_ENDPOINT_TOKEN}")
            # cabeçalho da requisição para obter o token
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            data = {
                'username': API_USERNAME_TOKEN,
                'password': API_PASSWORD_TOKEN
            
            }
            # utiliza requests para realizar a requisição na API, para obter o token
            response = requests.post(API_ENDPOINT_TOKEN, headers=headers, data=data, verify=API_SSL_VERIFY)

            # quando a requisição é bem-sucedida (status 200-299): O método não faz nada e o código continua normalmente.
            # quando a requisição falha (status fora de 200-299): Ele lança uma exceção requests.exceptions.HTTPError.
            response.raise_for_status()

            # monta o json com os dados retornados
            token_data = response.json()

            # A API retorna o token em um campo chamado 'access_token', verifica se o token foi retornado corretamente
            if 'access_token' not in token_data:
                msg = f"Erro ao obter token: 'access_token' não encontrado na resposta. {token_data}"
                logging.error(msg)
                raise KeyError(msg)
        
            # registra os dados do token na sessão
            session['access_token'] = token_data['access_token']
            session['expire_minutes'] = token_data['expire_minutes']
            session['token_type'] = token_data['token_type']
            session['token_validade'] = datetime.timestamp(datetime.now() + timedelta(minutes=token_data['expire_minutes']))

            logging.info(f"Token obtido com sucesso: {session['access_token']}, válido por {session['expire_minutes']} minutos.")
            # retorna o JSON do token obtido
            return token_data
    
        except Exception as e:
            # Se a exceção for do tipo HTTPError, pode-se acessar o código de status e a mensagem de erro
            if isinstance(e, requests.exceptions.HTTPError):
                msg = f"Erro HTTP: {e.response.status_code} - {e.response.text}"
            else:
                msg = f"Erro inesperado ao obter token: {e}"

            logging.error(msg)
            # retornar json com chave de erro e mensagem de erro
            return {'error': msg}, 500
        
    @staticmethod
    def validar_token():
        for _ in range(2): # Tenta obter o token no máximo 2 vezes
            if 'token_validade' in session and session['token_validade'] > datetime.timestamp(datetime.now()):
                # Token válido
                return True
                
            # Token inválido ou expirado, tenta obter um novo
            if 'access_token' in Funcoes.get_api_token():
                return True # Novo token obtido com sucesso
#       Se chegar aqui, significa que não foi possível obter um token válido
        return False
        
    @staticmethod
    def make_api_request(method, url, data=None, params=None):
    # verifica se tem um token dentro da validade
        if not Funcoes.validar_token():
            return {'error': 'Falha ao obter token de autenticação'}, 500
        
        headers = {
            'Authorization': f'Bearer {session["access_token"]}',
            'accept': 'application/json',
        }
        
        try:
            logging.info(f"Realizando requisição: {method.upper()} {url}")

            response = requests.request(method, url, headers=headers, json=data, params=params, verify=API_SSL_VERIFY)
            response.raise_for_status()

            result = response.json()
            return result[0] if response.content else {}, response.status_code

        except requests.exceptions.HTTPError as e:
            msg = f"Erro HTTP: {e.response.status_code} - {e.response.text}"
            logging.error(msg)
            return {'error': msg}, e.response.status_code
        except requests.exceptions.RequestException as e:
            msg = f"Erro de conexão/requisição com a API externa: {e}"
            logging.error(msg)
            return {'error': msg}, 500
        except Exception as e:
            msg = f"Erro inesperado ao processar requisição para API externa: {e}"
            logging.error(msg)
            return {'error': msg}, 500