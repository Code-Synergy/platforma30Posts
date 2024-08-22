from flask import Blueprint, request, jsonify
from . import db

ordens_de_servico_bp = Blueprint('ordens_de_servico', __name__)

class OrdemDeServico(db.Model):
    __tablename__ = 'ordens_de_servico'

    os_id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.pedido_id'))
    descricao = db.Column(db.String(255))
    responsavel_usuario_id = db.Column(db.Integer)
    workflow_id = db.Column(db.Integer, db.ForeignKey('workflow.workflow_id'))

    def __init__(self, pedido_id, descricao, responsavel_usuario_id, workflow_id):
        self.pedido_id = pedido_id
        self.descricao = descricao
        self.responsavel_usuario_id = responsavel_usuario_id
        self.workflow_id = workflow_id

@ordens_de_servico_bp.route('/', methods=['GET'])
def get_ordens_de_servico():
    ordens = OrdemDeServico.query.all()
    return jsonify([o.serialize() for o in ordens])

@ordens_de_servico_bp.route('/', methods=['POST'])
def add_ordem_de_servico():
    data = request.get_json()
    ordem = OrdemDeServico(
        pedido_id=data['pedido_id'],
        descricao=data.get('descricao'),
        responsavel_usuario_id=data.get('responsavel_usuario_id'),
        workflow_id=data.get('workflow_id')
    )
    db.session.add(ordem)
    db.session.commit()
    return jsonify(ordem.serialize()), 201

@ordens_de_servico_bp.route('/<int:id>', methods=['PUT'])
def update_ordem_de_servico(id):
    ordem = OrdemDeServico.query.get_or_404(id)
    data = request.get_json()

    ordem.descricao = data.get('descricao', ordem.descricao)
    ordem.responsavel_usuario_id = data.get('responsavel_usuario_id', ordem.responsavel_usuario_id)
    ordem.workflow_id = data.get('workflow_id', ordem.workflow_id)

    db.session.commit()
    return jsonify(ordem.serialize())

@ordens_de_servico_bp.route('/<int:id>', methods=['DELETE'])
def delete_ordem_de_servico(id):
    ordem = OrdemDeServico.query.get_or_404(id)
    db.session.delete(ordem)
    db.session.commit()
    return '', 204
