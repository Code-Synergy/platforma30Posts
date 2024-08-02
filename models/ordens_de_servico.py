from flask import Blueprint, request, jsonify
from . import get_db

ordens_de_servico_bp = Blueprint('ordens_de_servico', __name__)

@ordens_de_servico_bp.route('/', methods=['POST'])
def create_ordem_de_servico():
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO public.ordens_de_servico (
            negocio_id, indicacao, agencia, servico, formulario, 
            prazo_interno, prazo_externo, entrega, mensal, 
            responsavel, observacao
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
        RETURNING os_id;
    """, (
        data['negocio_id'], data['indicacao'], data['agencia'], data['servico'],
        data['formulario'], data['prazo_interno'], data['prazo_externo'],
        data['entrega'], data['mensal'], data['responsavel'], data['observacao']
    ))
    os_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return jsonify({'os_id': os_id}), 201

@ordens_de_servico_bp.route('/', methods=['GET'])
def get_ordens_de_servico():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM public.ordens_de_servico;")
    rows = cur.fetchall()
    cur.close()
    return jsonify(rows)

@ordens_de_servico_bp.route('/<int:id>', methods=['GET'])
def get_ordem_de_servico(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM public.ordens_de_servico WHERE os_id = %s;", (id,))
    row = cur.fetchone()
    cur.close()
    return jsonify(row)

@ordens_de_servico_bp.route('/<int:id>', methods=['PUT'])
def update_ordem_de_servico(id):
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE public.ordens_de_servico 
        SET negocio_id = %s, indicacao = %s, agencia = %s, servico = %s, 
            formulario = %s, prazo_interno = %s, prazo_externo = %s, entrega = %s, 
            mensal = %s, responsavel = %s, observacao = %s
        WHERE os_id = %s;
    """, (
        data['negocio_id'], data['indicacao'], data['agencia'], data['servico'],
        data['formulario'], data['prazo_interno'], data['prazo_externo'],
        data['entrega'], data['mensal'], data['responsavel'], data['observacao'], id
    ))
    conn.commit()
    cur.close()
    return jsonify({'message': 'Ordem de Serviço atualizada com sucesso'}), 200

@ordens_de_servico_bp.route('/<int:id>', methods=['DELETE'])
def delete_ordem_de_servico(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM public.ordens_de_servico WHERE os_id = %s;", (id,))
    conn.commit()
    cur.close()
    return jsonify({'message': 'Ordem de Serviço deletada com sucesso'}), 200
