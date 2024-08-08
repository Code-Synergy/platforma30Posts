from flask import Blueprint, request, jsonify
from . import get_db

informacoes_clientes_bp = Blueprint('informacoes_clientes', __name__)


# Criar informação de cliente
@informacoes_clientes_bp.route('/', methods=['POST'])
def create_informacao_cliente():
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO public.informacoes_clientes (cliente_id, ano_id, id_cliente, id_pedido, id_os, servico, valor) 
        VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING info_id;
    """, (data['cliente_id'], data['ano_id'], data['id_cliente'], data['id_pedido'], data['id_os'], data['servico'],
          data['valor']))
    info_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return jsonify({'info_id': info_id}), 201


# Obter todas as informações de clientes
@informacoes_clientes_bp.route('/', methods=['GET'])
def get_informacoes_clientes():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM public.informacoes_clientes;")
    rows = cur.fetchall()
    cur.close()
    return jsonify(rows)


# Obter uma informação específica de cliente
@informacoes_clientes_bp.route('/<int:id>', methods=['GET'])
def get_informacao_cliente(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM public.informacoes_clientes WHERE info_id = %s;", (id,))
    row = cur.fetchone()
    cur.close()
    return jsonify(row)


# Atualizar uma informação de cliente
@informacoes_clientes_bp.route('/<int:id>', methods=['PUT'])
def update_informacao_cliente(id):
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM public.informacoes_clientes WHERE info_id = %s;", (id,))
    info_atual = cur.fetchone()

    if not info_atual:
        return jsonify({'message': 'Informação não encontrada'}), 404

    cliente_id = data.get('cliente_id', info_atual[1])
    ano_id = data.get('ano_id', info_atual[2])
    id_cliente = data.get('id_cliente', info_atual[3])
    id_pedido = data.get('id_pedido', info_atual[4])
    id_os = data.get('id_os', info_atual[5])
    servico = data.get('servico', info_atual[6])
    valor = data.get('valor', info_atual[7])

    cur.execute("""
        UPDATE public.informacoes_clientes 
        SET cliente_id = %s, ano_id = %s, id_cliente = %s, id_pedido = %s, id_os = %s, servico = %s, valor = %s 
        WHERE info_id = %s;
    """, (cliente_id, ano_id, id_cliente, id_pedido, id_os, servico, valor, id))

    conn.commit()
    cur.close()
    return jsonify({'message': 'Informação de cliente atualizada com sucesso'}), 200


# Deletar uma informação de cliente
@informacoes_clientes_bp.route('/<int:id>', methods=['DELETE'])
def delete_informacao_cliente(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM public.informacoes_clientes WHERE info_id = %s;", (id,))
    conn.commit()
    cur.close()
    return jsonify({'message': 'Informação de cliente deletada com sucesso'}), 200
