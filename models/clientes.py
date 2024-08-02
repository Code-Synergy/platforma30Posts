from flask import Blueprint, request, jsonify
from . import get_db

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/', methods=['POST'])
def create_cliente():
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO public.clientes (nome, contato, segmento, telefone, email, pais) 
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING cliente_id;
    """, (data['nome'], data['contato'], data['segmento'], data['telefone'], data['email'], data['pais']))
    cliente_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return jsonify({'cliente_id': cliente_id}), 201

@clientes_bp.route('/', methods=['GET'])
def get_clientes():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM public.clientes;")
    rows = cur.fetchall()
    cur.close()
    return jsonify(rows)

@clientes_bp.route('/<int:id>', methods=['GET'])
def get_cliente(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM public.clientes WHERE cliente_id = %s;", (id,))
    row = cur.fetchone()
    cur.close()
    return jsonify(row)

@clientes_bp.route('/<int:id>', methods=['PUT'])
def update_cliente(id):
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE public.clientes 
        SET nome = %s, contato = %s, segmento = %s, telefone = %s, email = %s, pais = %s 
        WHERE cliente_id = %s;
    """, (data['nome'], data['contato'], data['segmento'], data['telefone'], data['email'], data['pais'], id))
    conn.commit()
    cur.close()
    return jsonify({'message': 'Cliente atualizado com sucesso'}), 200

@clientes_bp.route('/<int:id>', methods=['DELETE'])
def delete_cliente(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM public.clientes WHERE cliente_id = %s;", (id,))
    conn.commit()
    cur.close()
    return jsonify({'message': 'Cliente deletado com sucesso'}), 200
