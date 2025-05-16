from flask import Blueprint, jsonify, request, make_response
from settings import API_ENDPOINT_FUNCIONARIO
from funcoes import Funcoes
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

# Rota para Criar um novo Funcionário (POST)
@bp_funcionario.route('/', methods=['POST'])
def create_funcionario():
    # verifica se o conteúdo da requisição é JSON
    if not request.is_json:
        return jsonify({"error": "Requisição deve ser JSON"}), 400
    
    # obtém o corpo da requisição JSON
    data = request.get_json()
    
    # validação básica para ver se os campos foram informados no json
    required_fields = ['nome', 'matricula', 'cpf', 'senha', 'grupo', 'telefone']
    if not all(field in data for field in required_fields):
        return jsonify({"error": f"Campos obrigatórios faltando: {required_fields}"}), 400
    
    # Cria um novo dicionário para não alterar o original
    processed_data = data.copy()
    
    # Hash da senha antes de enviar para a API
    if 'senha' in processed_data:
        processed_data['senha'] = hash_password(processed_data['senha'])
    
    # chama a função para fazer a requisição à API externa
    response_data, status_code = Funcoes.make_api_request('post', API_ENDPOINT_FUNCIONARIO, data=processed_data)
    
    # retorna o json da resposta da API externa
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

    # Se campo senha estiver vazio ou ausente, sinaliza para manter a senha antiga
    if 'senha' not in processed_data or not processed_data.get('senha'):
        processed_data['manter_senha'] = True
        processed_data.pop('senha', None)
    else:
        # Se senha foi passada, hash antes de enviar
        processed_data['senha'] = hash_password(processed_data['senha'])

    # Monta URL da API real com o ID no path conforme especificação
    response_data, status_code = Funcoes.make_api_request(
        'put',
        f"{API_ENDPOINT_FUNCIONARIO}{id_funcionario}",
        data=processed_data
    )

    return jsonify(response_data), status_code


# Rota para Validar o Login (POST)
@bp_funcionario.route('/login', methods=['POST'])
def validar_login():
    # verifica se o conteúdo da requisição é JSON
    if not request.is_json:
        return jsonify({"error": "Requisição deve ser JSON"}), 400
    
    # obtem o corpo da requisição JSON
    data = request.get_json()
    
    # validação básica para ver se os campos foram informados no json
    required_fields = ['cpf', 'senha']
    if not all(field in data for field in required_fields):
        return jsonify({"error": f"Campos obrigatórios faltando: {required_fields}"}), 400
    
    # chama a função para fazer a requisição à API externa
    response_data, status_code = Funcoes.make_api_request('post', f"{API_ENDPOINT_FUNCIONARIO}login/", data=data)
    
    # retorna o json da resposta da API externa
    return jsonify(response_data), status_code

