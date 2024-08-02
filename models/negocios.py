from flask import Blueprint, request, jsonify
from . import get_db

negocios_bp = Blueprint('negocios', __name__)

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

@negocios_bp.route('/', methods=['GET'])
def get_negocios():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM public.negocios;")
    rows = cur.fetchall()
    cur.close()
    return jsonify(rows)

@negocios_bp.route('/<int:id>', methods=['GET'])
def get_negocio(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM public.negocios WHERE negocio_id = %s;", (id,))
    row = cur.fetchone()
    cur.close()
    return jsonify(row)

@negocios_bp.route('/<int:id>', methods=['PUT'])
def update_negocio(id):
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE public.negocios 
        SET cliente_id = %s, nome_negocio = %s, descricao = %s 
        WHERE negocio_id = %s;
    """, (data['cliente_id'], data['nome_negocio'], data['descricao'], id))
    conn.commit()
    cur.close()
    return jsonify({'message': 'Negócio atualizado com sucesso'}), 200

@negocios_bp.route('/<int:id>', methods=['DELETE'])
def delete_negocio(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM public.negocios WHERE negocio_id = %s;", (id,))
    conn.commit()
    cur.close()
    return jsonify({'message': 'Negócio deletado com sucesso'}), 200
