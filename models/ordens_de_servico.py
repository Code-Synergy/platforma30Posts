from flask import Blueprint, request, jsonify
from . import db

ordens_de_servico_bp = Blueprint('ordens_de_servico', __name__)

class OrdemDeServico(db.Model):
    __tablename__ = 'ordens_de_servico'

    ordem_id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    data = db.Column(db.Date, nullable=False)
    usuario_id = db.Column(db.Integer, nullable=False)
    workflow_id = db.Column(db.Integer, nullable=False)
    id_form = db.Column(db.Integer, nullable=True)

    def __init__(self, pedido_id, descricao, data, usuario_id, workflow_id, id_form):
        self.pedido_id = pedido_id
        self.descricao = descricao
        self.data = data
        self.usuario_id = usuario_id
        self.workflow_id = workflow_id
        self.id_form = id_form

    def serialize(self):
        return {
            'ordem_id': self.ordem_id,
            'pedido_id': self.pedido_id,
            'descricao': self.descricao,
            'data': self.data,
            'usuario_id': self.usuario_id,
            'workflow_id': self.workflow_id,
            'id_form': self.id_form
        }

# Rotas para as operações CRUD
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
        data=data.get('data'),
        usuario_id=data.get('usuario_id'),
        workflow_id=data.get('workflow_id'),
        id_form=data.get('id_form')
    )
    db.session.add(ordem)
    db.session.commit()
    return jsonify(ordem.serialize()), 201

@ordens_de_servico_bp.route('/<int:id>', methods=['PUT'])
def update_ordem_de_servico(id):
    ordem = OrdemDeServico.query.get_or_404(id)
    data = request.get_json()

    ordem.descricao = data.get('descricao', ordem.descricao)
    ordem.data = data.get('data', ordem.data)
    ordem.usuario_id = data.get('usuario_id', ordem.usuario_id)
    ordem.workflow_id = data.get('workflow_id', ordem.workflow_id)
    ordem.id_form = data.get('id_form', ordem.id_form)

    db.session.commit()
    return jsonify(ordem.serialize())

@ordens_de_servico_bp.route('/<int:id>', methods=['DELETE'])
def delete_ordem_de_servico(id):
    ordem = OrdemDeServico.query.get_or_404(id)
    db.session.delete(ordem)
    db.session.commit()
    return '', 204
