from flask import Blueprint, jsonify, request, make_response
from settings import API_ENDPOINT_FUNCIONARIO
from funcoes import Funcoes
import logging
from security import hash_password,verify_password
from flask_cors import cross_origin


bp_funcionario = Blueprint('funcionario', __name__, url_prefix="/api/funcionario")

# Rota para Listar todos os Funcionários (READ - All)
@bp_funcionario.route('/all', methods=['GET'])
def get_funcionarios():
    # Chama a função para fazer a requisição à API externa
    response_data, status_code = Funcoes.make_api_request('get', API_ENDPOINT_FUNCIONARIO)
    # Retorna o JSON da resposta da API externa
    return jsonify(response_data), status_code

# Rota para Obter um Funcionário Específico (READ - One)
@bp_funcionario.route('/one', methods=['GET'])
def get_funcionario():
    # obtém o ID do funcionário a partir dos parâmetros de consulta da URL
    id_funcionario = request.args.get('id_funcionario')
    # valida se o id_funcionario foi passado na URL
    if not id_funcionario:
        return jsonify({"error": "O parâmetro 'id_funcionario' é obrigatório"}), 400
    # chama a função para fazer a requisição à API externa
    response_data, status_code = Funcoes.make_api_request('get', f"{API_ENDPOINT_FUNCIONARIO}{id_funcionario}")
    # retorna o json da resposta da API externa
    return jsonify(response_data), status_code

@bp_funcionario.route('/', methods=['POST'])
def create_funcionario():
    if not request.is_json:
        return jsonify({"error": "Requisição deve ser JSON"}), 400

    data = request.get_json()

    required_fields = ['nome', 'matricula', 'cpf', 'senha', 'grupo', 'telefone']
    if not all(field in data for field in required_fields):
        return jsonify({"error": f"Campos obrigatórios faltando: {required_fields}"}), 400
    
    processed_data = data.copy() # Copia os dados, mas sem manipular a senha aqui

    # Chama a função para fazer a requisição à API externa
    # O FastAPI esperará a senha em texto plano e a hasheará antes de salvar
    response_data, status_code = Funcoes.make_api_request('post', API_ENDPOINT_FUNCIONARIO, data=processed_data)

    return jsonify(response_data), status_code

# Rota para Deletar um Funcionário (DELETE)
@bp_funcionario.route('/', methods=['DELETE'])
def delete_funcionario():
    # obtém o ID do funcionário a partir dos parâmetros de consulta da URL
    id_funcionario = request.args.get('id_funcionario')
    # valida se o id_funcionario foi passado na URL
    if not id_funcionario:
        return jsonify({"error": "O parâmetro 'id_funcionario' é obrigatório"}), 400
    # chama a função para fazer a requisição à API externa
    response_data, status_code = Funcoes.make_api_request('delete', f"{API_ENDPOINT_FUNCIONARIO}{id_funcionario}")
    # retorna o json da resposta da API externa
    return jsonify(response_data), status_code

@bp_funcionario.route('/check-cpf', methods=['GET'])
def check_cpf_exists():
    # obtém o CPF a partir dos parâmetros de consulta da URL
    cpf = request.args.get('cpf')
    # valida se o CPF foi passado na URL
    if not cpf:
        return jsonify({"error": "O parâmetro 'cpf' é obrigatório"}), 400
    # chama a função para fazer a requisição à API externa
    response_data, status_code = Funcoes.make_api_request('get', f"{API_ENDPOINT_FUNCIONARIO}cpf/{cpf}")
    # retorna o json da resposta da API externa
    return jsonify(response_data), status_code

@bp_funcionario.route('/', methods=['PUT'])
def update_funcionario():
    if not request.is_json:
        return jsonify({"error": "Requisição deve ser JSON"}), 400

    data = request.get_json()
    id_funcionario = data.get('id_funcionario')

    required_fields = ['id_funcionario', 'nome', 'matricula', 'cpf', 'grupo', 'telefone']
    if not id_funcionario:
        return jsonify({"error": "Campo 'id_funcionario' obrigatório no corpo JSON"}), 400

    if not all(field in data for field in required_fields):
        return jsonify({"error": f"Campos obrigatórios faltando: {required_fields}"}), 400

    processed_data = data.copy()

    # CORREÇÃO: Se campo senha estiver vazio ou ausente, OU se manter_senha for True
    if 'manter_senha' in processed_data and processed_data.get('manter_senha'):
        # Remove tanto 'senha' quanto 'manter_senha' do payload para a API
        processed_data.pop('senha', None)
        processed_data.pop('manter_senha', None)
    elif 'senha' not in processed_data or not processed_data.get('senha'):
        # Se não tem senha ou está vazia, também remove
        processed_data.pop('senha', None)

    print(f"DEBUG: Dados processados antes da API: {processed_data}")  # DEBUG

    response_data, status_code = Funcoes.make_api_request(
        'put',
        f"{API_ENDPOINT_FUNCIONARIO}{id_funcionario}",
        data=processed_data
    )

    print(f"DEBUG: Resposta da API: {response_data}, Status: {status_code}")  # DEBUG

    return jsonify(response_data), status_code


@bp_funcionario.route('/login', methods=['POST'])
def validar_login():
    if not request.is_json:
        return jsonify({"error": "Requisição deve ser JSON"}), 400

    data = request.get_json()
    
    # Log dos dados recebidos para debug
    logging.info(f"Dados recebidos no proxy para login: CPF={data.get('cpf', 'N/A')}")
    
    required_fields = ['cpf', 'senha']
    if not all(field in data for field in required_fields):
        return jsonify({"error": f"Campos obrigatórios faltando: {required_fields}"}), 400

    try:
        # IMPORTANTE: require_auth=False para endpoint de login
        response_data, status_code = Funcoes.make_api_request(
            'post', 
            f"{API_ENDPOINT_FUNCIONARIO}login/", 
            data=data,
            require_auth=False  # Login não precisa de autenticação prévia
        )
        
        logging.info(f"Resposta da API login: Status {status_code}")
        
        # Se login bem-sucedido, pode salvar token na sessão se necessário
        if status_code == 200 and 'token' in response_data:
            logging.info("Login realizado com sucesso")
        
        return jsonify(response_data), status_code
        
    except Exception as e:
        logging.error(f"Erro no proxy login: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Erro interno do servidor"}), 500