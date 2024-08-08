from flask import Blueprint, request, jsonify
from . import get_db

negocios_bp = Blueprint('negocios', __name__)


# Criar negócio
@negocios_bp.route('/', methods=['POST'])
def create_negocio():
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO public.negocios (cliente_id, nome_negocio, descricao) 
        VALUES (%s, %s, %s) RETURNING negocio_id;
    """, (data['cliente_id'], data['nome_negocio'], data['descricao']))
    negocio_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return jsonify({'negocio_id': negocio_id}), 201


# Obter todos os negócios
@negocios_bp.route('/', methods=['GET'])
def get_negocios():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM public.negocios;")
    rows = cur.fetchall()
    cur.close()
    return jsonify(rows)


# Obter um negócio específico
@negocios_bp.route('/<int:id>', methods=['GET'])
def get_negocio(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM public.negocios WHERE negocio_id = %s;", (id,))
    row = cur.fetchone()
    cur.close()
    return jsonify(row)


# Atualizar um negócio
@negocios_bp.route('/<int:id>', methods=['PUT'])
def update_negocio(id):
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM public.negocios WHERE negocio_id = %s;", (id,))
    negocio_atual = cur.fetchone()

    if not negocio_atual:
        return jsonify({'message': 'Negócio não encontrado'}), 404

    cliente_id = data.get('cliente_id', negocio_atual[1])
    nome_negocio = data.get('nome_negocio', negocio_atual[2])
    descricao = data.get('descricao', negocio_atual[3])

    cur.execute("""
        UPDATE public.negocios 
        SET cliente_id = %s, nome_negocio = %s, descricao = %s 
        WHERE negocio_id = %s;
    """, (cliente_id, nome_negocio, descricao, id))

    conn.commit()
    cur.close()
    return jsonify({'message': 'Negócio atualizado com sucesso'}), 200


# Deletar um negócio
@negocios_bp.route('/<int:id>', methods=['DELETE'])
def delete_negocio(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM public.negocios WHERE negocio_id = %s;", (id,))
    conn.commit()
    cur.close()
    return jsonify({'message': 'Negócio deletado com sucesso'}), 200
