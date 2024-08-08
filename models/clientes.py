from flask import Blueprint, request, jsonify
from . import get_db

clientes_bp = Blueprint('clientes', __name__)


# Criar cliente
@clientes_bp.route('/', methods=['POST'])
def create_cliente():
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO public.clientes (nome, contato, segmento, telefone, email, pais, negocio_id, ativo) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING cliente_id;
    """, (
    data['nome'], data['contato'], data['segmento'], data['telefone'], data['email'], data['pais'], data['negocio_id'],
    True))
    cliente_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return jsonify({'cliente_id': cliente_id}), 201


# Obter todos os clientes ativos
@clientes_bp.route('/', methods=['GET'])
def get_clientes():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM public.clientes WHERE ativo = TRUE;")
    rows = cur.fetchall()
    cur.close()
    return jsonify(rows)


# Obter um cliente específico
@clientes_bp.route('/<int:id>', methods=['GET'])
def get_cliente(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM public.clientes WHERE cliente_id = %s AND ativo = TRUE;", (id,))
    row = cur.fetchone()
    cur.close()
    return jsonify(row)


# Atualizar cliente
@clientes_bp.route('/<int:id>', methods=['PUT'])
def update_cliente(id):
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()

    # Obter o cliente atual
    cur.execute("SELECT * FROM public.clientes WHERE cliente_id = %s;", (id,))
    cliente_atual = cur.fetchone()

    if not cliente_atual:
        return jsonify({'message': 'Cliente não encontrado'}), 404

    # Atualizar apenas os campos fornecidos no JSON
    nome = data.get('nome', cliente_atual[1])
    contato = data.get('contato', cliente_atual[2])
    segmento = data.get('segmento', cliente_atual[3])
    telefone = data.get('telefone', cliente_atual[4])
    email = data.get('email', cliente_atual[5])
    pais = data.get('pais', cliente_atual[6])
    negocio_id = data.get('negocio_id', cliente_atual[7])
    ativo = data.get('ativo', cliente_atual[8])

    cur.execute("""
        UPDATE public.clientes 
        SET nome = %s, contato = %s, segmento = %s, telefone = %s, email = %s, pais = %s, negocio_id = %s, ativo = %s 
        WHERE cliente_id = %s;
    """, (nome, contato, segmento, telefone, email, pais, negocio_id, ativo, id))

    conn.commit()
    cur.close()
    return jsonify({'message': 'Cliente atualizado com sucesso'}), 200


# Desativar cliente (exclusão lógica)
@clientes_bp.route('/<int:id>', methods=['DELETE'])
def delete_cliente(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE public.clientes SET ativo = FALSE WHERE cliente_id = %s;", (id,))
    conn.commit()
    cur.close()
    return jsonify({'message': 'Cliente desativado com sucesso'}), 200
