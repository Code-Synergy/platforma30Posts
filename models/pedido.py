from flask import Blueprint, request, jsonify
from . import db

pedidos_bp = Blueprint('pedidos', __name__)

def serialize_pedido(pedido):
    return {
        'pedido_id': pedido[0],
        'negocio_id': pedido[1],
        'descricao': pedido[2],
        'valor': float(pedido[3])
    }

@pedidos_bp.route('/', methods=['GET'])
def get_pedidos():
    try:
        conn = db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM public.pedidos;")
        pedidos = cur.fetchall()
        cur.close()
        return jsonify([serialize_pedido(p) for p in pedidos]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pedidos_bp.route('/', methods=['POST'])
def create_pedido():
    data = request.get_json()
    try:
        conn = db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO public.pedidos (negocio_id, descricao, valor)
            VALUES (%s, %s, %s)
            RETURNING pedido_id;
        """, (
            data['negocio_id'], data.get('descricao'), data['valor']
        ))
        pedido_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return jsonify({'pedido_id': pedido_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pedidos_bp.route('/<int:id>/', methods=['PUT'])
def update_pedido(id):
    data = request.get_json()
    try:
        conn = db()
        cur = conn.cursor()
        cur.execute("""
            UPDATE public.pedidos
            SET negocio_id = %s, descricao = %s, valor = %s
            WHERE pedido_id = %s;
        """, (
            data['negocio_id'], data.get('descricao'), data['valor'], id
        ))
        conn.commit()
        cur.close()
        return jsonify({'message': 'Pedido atualizado com sucesso'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pedidos_bp.route('/<int:id>/', methods=['DELETE'])
def delete_pedido(id):
    try:
        conn = db()
        cur = conn.cursor()
        cur.execute("DELETE FROM public.pedidos WHERE pedido_id = %s;", (id,))
        conn.commit()
        cur.close()
        return jsonify({'message': 'Pedido deletado com sucesso'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
