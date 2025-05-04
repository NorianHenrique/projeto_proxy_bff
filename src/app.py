import os
from flask import Flask, send_from_directory, session
from datetime import timedelta
from flask_cors import CORS
import logging
from settings import PROXY_PORT, PROXY_DEBUG, TEMPO_SESSION, FRONTEND_URL  # carrega o arquivo .env, variáveis de ambiente
from funcoes import Funcoes
from mod_funcionario.funcionario import bp_funcionario
from mod_cliente.cliente import bp_cliente
from mod_produto.produto import bp_produto
# Configuração básica de logging
logging.basicConfig(level=logging.INFO)

# Aplicação Flask
app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": f"{FRONTEND_URL}"}})

# Rota para o favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        directory='static',
        path='favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

# Rota para teste de comunicação com a API e geração do token
@app.route('/api/teste_token', methods=['POST'])
def teste_token():
    return Funcoes.get_api_token()

# Gerando uma chave randômica para secret_key
app.secret_key = os.urandom(12).hex()
# Configuração do tempo de expiração da sessão
app.permanent_session_lifetime = timedelta(minutes=int(TEMPO_SESSION))
# Configuração do SameSite para cookies
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
# Configuração para enviar cookies apenas em conexões HTTPS
app.config['SESSION_COOKIE_SECURE'] = True

# Decorador @app.before_request
@app.before_request
def before_request():
    session.permanent = True

# Registrando o blueprint do funcionário
app.register_blueprint(bp_funcionario)
# Registrando o blueprint do cliente
app.register_blueprint(bp_cliente)
# Registrando o blueprint do produto
app.register_blueprint(bp_produto)

# Ponto de entrada para execução
if __name__ == '__main__':
    logging.info(f"Iniciando o servidor Flask na porta: {PROXY_PORT}")
    app.run(host='0.0.0.0', port=PROXY_PORT, debug=PROXY_DEBUG, use_reloader=PROXY_DEBUG)
