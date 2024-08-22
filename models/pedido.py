from flask import Blueprint, request, jsonify
from . import get_db

pedidos_bp = Blueprint('pedidos', __name__)

@pedidos_bp.route('/', methods=['GET'])
def get_pedidos():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM public.pedidos;")
    pedidos = cur.fetchall()
    cur.close()
    return jsonify(pedidos), 200

@pedidos_bp.route('/', methods=['POST'])
def create_pedido():
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO public.pedidos (negocio_id, descricao, valor)
        VALUES (%s, %s, %s)
        RETURNING pedido_id;
    """, (
        data['negocio_id'], data['descricao'], data['valor']
    ))
    pedido_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return jsonify({'pedido_id': pedido_id}), 201

@pedidos_bp.route('/<int:id>/', methods=['PUT'])
def update_pedido(id):
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE public.pedidos
        SET negocio_id = %s, descricao = %s, valor = %s
        WHERE pedido_id = %s;
    """, (
        data['negocio_id'], data['descricao'], data['valor'], id
    ))
    conn.commit()
    cur.close()
    return jsonify({'message': 'Pedido atualizado com sucesso'}), 200

@pedidos_bp.route('/<int:id>/', methods=['DELETE'])
def delete_pedido(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM public.pedidos WHERE pedido_id = %s;", (id,))
    conn.commit()
    cur.close()
    return jsonify({'message': 'Pedido deletado com sucesso'}), 200
