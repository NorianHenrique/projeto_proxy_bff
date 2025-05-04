
from flask import Blueprint, jsonify, request
from settings import API_ENDPOINT_CLIENTE
from funcoes import Funcoes

bp_cliente = Blueprint('cliente', __name__, url_prefix="/api/cliente")

# Rota para Listar todos os Clientes (READ - All)
@bp_cliente.route('/all', methods=['GET'])
def get_clientes():
    # Chama a função para fazer a requisição à API externa
    response_data, status_code = Funcoes.make_api_request('get', API_ENDPOINT_CLIENTE)
    # Retorna o JSON da resposta da API externa
    return jsonify(response_data), status_code

# Rota para Obter um Cliente Específico (READ - One)
@bp_cliente.route('/one', methods=['GET'])
def get_cliente():
    # obtém o ID do cliente a partir dos parâmetros de consulta da URL
    id_cliente = request.args.get('id_cliente')
    # valida se o id_cliente foi passado na URL
    if not id_cliente:
        return jsonify({"error": "O parâmetro 'id_cliente' é obrigatório"}), 400
    # chama a função para fazer a requisição à API externa
    response_data, status_code = Funcoes.make_api_request('get', f"{API_ENDPOINT_CLIENTE}{id_cliente}")
    # retorna o json da resposta da API externa
    return jsonify(response_data), status_code

# Rota para Criar um novo Cliente (POST)
@bp_cliente.route('/', methods=['POST'])
def create_cliente():
    # verifica se o conteúdo da requisição é JSON
    if not request.is_json:
        return jsonify({"error": "Requisição deve ser JSON"}), 400
        # obtém o corpo da requisição JSON
    data = request.get_json()
    # validação básica para ver se os campos foram informados no json
    required_fields = ['nome', 'cpf', 'telefone']
    if not all(field in data for field in required_fields):
        return jsonify({"error": f"Campos obrigatórios faltando: {required_fields}"}), 400
    # chama a função para fazer a requisição à API externa
    response_data, status_code = Funcoes.make_api_request('post', API_ENDPOINT_CLIENTE, data=data)
    # retorna o json da resposta da API externa
    return jsonify(response_data), status_code

# Rota para Atualizar um Cliente existente (PUT)
@bp_cliente.route('/', methods=['PUT'])
def update_cliente():
    # verifica se o conteúdo da requisição é JSON
    if not request.is_json:
        return jsonify({"error": "Requisição deve ser JSON"}), 400
    # obtém o corpo da requisição JSON
    data = request.get_json()
    # validação básica para ver se os campos foram informados no json
    required_fields = ['id_cliente', 'nome', 'cpf', 'telefone']
    if not all(field in data for field in required_fields):
        return jsonify({"error": f"Campos obrigatórios faltando: {required_fields}"}), 400
    # chama a função para fazer a requisição à API externa
    response_data, status_code = Funcoes.make_api_request('put', f"{API_ENDPOINT_CLIENTE}{data.get('id_cliente')}", data=data)
    # retorna o json da resposta da API externa
    return jsonify(response_data), status_code

# Rota para Deletar um Cliente (DELETE)
@bp_cliente.route('/', methods=['DELETE'])
def delete_cliente():
    # obtém o ID do cliente a partir dos parâmetros de consulta da URL
    id_cliente = request.args.get('id_cliente')
    # valida se o id_cliente foi passado na URL
    if not id_cliente:
        return jsonify({"error": "O parâmetro 'id_cliente' é obrigatório"}), 400
    # chama a função para fazer a requisição à API externa
    response_data, status_code = Funcoes.make_api_request('delete', f"{API_ENDPOINT_CLIENTE}{id_cliente}")
    # retorna o json da resposta da API externa
    return jsonify(response_data), status_code

# Rota para Validar se CPF já existe (GET)
@bp_cliente.route('/cpf', methods=['GET'])
def validate_cpf():
    # obtém o CPF a partir dos parâmetros de consulta da URL
    cpf = request.args.get('cpf')
    # valida se o CPF foi passado na URL
    if not cpf:
        return jsonify({"error": "O parâmetro 'cpf' é obrigatório"}), 400
    # chama a função para fazer a requisição à API externa
    response_data, status_code = Funcoes.make_api_request('get', f"{API_ENDPOINT_CLIENTE}cpf/{cpf}")
    # retorna o json da resposta da API externa
    return jsonify(response_data), status_code
