from flask_cors import cross_origin
from flask import Blueprint, jsonify, request
from settings import API_ENDPOINT_PRODUTO
from funcoes import Funcoes

import base64

bp_produto = Blueprint('produto', __name__, url_prefix="/api/produto")

# Rota para Listar todos os Produtos (READ - All)
@bp_produto.route('/all', methods=['GET'])
def get_produtos():
    # Chama a função para fazer a requisição à API externa
    response_data, status_code = Funcoes.make_api_request('get', API_ENDPOINT_PRODUTO)
    # Retorna o JSON da resposta da API externa
    return jsonify(response_data), status_code

# Rota para Obter um Produto Específico (READ - One)
@bp_produto.route('/one', methods=['GET'])
def get_produto():
    # obtém o ID do produto a partir dos parâmetros de consulta da URL
    id_produto = request.args.get('id_produto')
    # valida se o id_produto foi passado na URL
    if not id_produto:
        return jsonify({"error": "O parâmetro 'id_produto' é obrigatório"}), 400
    # chama a função para fazer a requisição à API externa
    response_data, status_code = Funcoes.make_api_request('get', f"{API_ENDPOINT_PRODUTO}{id_produto}")
    # retorna o json da resposta da API externa
    return jsonify(response_data), status_code

# Rota para Criar um novo Produto (POST)
@bp_produto.route('/', methods=['POST'])
def create_produto():
    # obtém a foto enviada no formulário
    # o arquivo deve ter sido enviado como multipart/form-data
    foto = request.files.get('foto')
    # Converte a foto para Base64
    # realiza a leitura do conteúdo do arquivo com a foto
    foto_data = foto.read()
    # converte para Base64
    foto_base64 = base64.b64encode(foto_data).decode('utf-8')
    # adiciona o prefixo para indicar o tipo de arquivo
    foto_base64 = f"data:{foto.mimetype};base64,{foto_base64}"

    # Monta o JSON para enviar à API externa
    data = {
        "nome": request.form.get('nome'),
        "descricao": request.form.get('descricao'),
        "valor_unitario": request.form.get('valor_unitario'),
        "foto": foto_base64
        }
    # Faz a requisição à API externa
    response_data, status_code = Funcoes.make_api_request('post', API_ENDPOINT_PRODUTO, data=data)
    # Retorna o JSON da resposta da API externa
    return jsonify(response_data), status_code

# Rota para Atualizar um Produto existente (PUT)
@bp_produto.route('/', methods=['PUT'])
def update_produto():
    foto = request.files.get('foto')

    if foto:
        foto_data = foto.read()
        # Corrigido encoding e uso correto do base64
        foto_base64 = base64.b64encode(foto_data).decode('utf-8')
        foto_base64 = f"data:{foto.mimetype};base64,{foto_base64}"
    else:
        foto_base64 = request.form.get('foto')

    data = {
        "id_produto": request.form.get('id_produto'),
        "nome": request.form.get('nome'),
        "descricao": request.form.get('descricao'),
        "valor_unitario": request.form.get('valor_unitario'),
        "foto": foto_base64
    }

    response_data, status_code = Funcoes.make_api_request('put', f"{API_ENDPOINT_PRODUTO}{data.get('id_produto')}", data=data)
    return jsonify(response_data), status_code


# Rota para Deletar um Produto (DELETE)
@bp_produto.route('/', methods=['DELETE'])
def delete_produto():
    # obtém o ID do produto a partir dos parâmetros de consulta da URL
    id_produto = request.args.get('id_produto')
    # valida se o id_produto foi passado na URL
    if not id_produto:
        return jsonify({"error": "O parâmetro 'id_produto' é obrigatório"}), 400
    # chama a função para fazer a requisição à API externa
    response_data, status_code = Funcoes.make_api_request('delete', f"{API_ENDPOINT_PRODUTO}{id_produto}")
    # retorna o json da resposta da API externa
    return jsonify(response_data), status_code

# Rota para Validar se Produto já existe (GET)
@bp_produto.route('/nome', methods=['GET'])
def validate_nome():
    # obtém o Nome a partir dos parâmetros de consulta da URL
    nome = request.args.get('nome')
    # valida se o produto foi passado na URL
    if not nome:
        return jsonify({"error": "O parâmetro 'nome' é obrigatório"}), 400
    # chama a função para fazer a requisição à API externa
    response_data, status_code = Funcoes.make_api_request('get', f"{API_ENDPOINT_PRODUTO}nome/{nome}")
    # retorna o json da resposta da API externa
    return jsonify(response_data), status_code

