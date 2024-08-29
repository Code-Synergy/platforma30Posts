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
    id_form = db.Column(db.String(36), nullable=True)
    id_negocio = db.Column(db.Integer, nullable=True)
    indicacao = db.Column(db.Text, nullable=True)
    agencia = db.Column(db.Text, nullable=True)
    id_produto = db.Column(db.Integer, nullable=True)
    prazointerno = db.Column(db.Date, nullable=True)
    prazoexterno = db.Column(db.Date, nullable=True)
    entrega = db.Column(db.Date, nullable=True)
    mensal = db.Column(db.Boolean, nullable=True)
    responsavel = db.Column(db.Integer, nullable=True)
    observacao = db.Column(db.Text, nullable=True)

    def __init__(self, pedido_id, descricao, data, usuario_id, workflow_id, id_form=None, id_negocio=None, indicacao=None,
                 agencia=None, id_produto=None, prazointerno=None, prazoexterno=None, entrega=None, mensal=None,
                 responsavel=None, observacao=None):
        self.pedido_id = pedido_id
        self.descricao = descricao
        self.data = data
        self.usuario_id = usuario_id
        self.workflow_id = workflow_id
        self.id_form = id_form
        self.id_negocio = id_negocio
        self.indicacao = indicacao
        self.agencia = agencia
        self.id_produto = id_produto
        self.prazointerno = prazointerno
        self.prazoexterno = prazoexterno
        self.entrega = entrega
        self.mensal = mensal
        self.responsavel = responsavel
        self.observacao = observacao

    def serialize(self):
        return {
            'ordem_id': self.ordem_id,
            'pedido_id': self.pedido_id,
            'descricao': self.descricao,
            'data': self.data,
            'usuario_id': self.usuario_id,
            'workflow_id': self.workflow_id,
            'id_form': self.id_form,
            'id_negocio': self.id_negocio,
            'indicacao': self.indicacao,
            'agencia': self.agencia,
            'id_produto': self.id_produto,
            'prazointerno': self.prazointerno,
            'prazoexterno': self.prazoexterno,
            'entrega': self.entrega,
            'mensal': self.mensal,
            'responsavel': self.responsavel,
            'observacao': self.observacao
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
        id_form=data.get('id_form'),
        id_negocio=data.get('id_negocio'),
        indicacao=data.get('indicacao'),
        agencia=data.get('agencia'),
        id_produto=data.get('id_produto'),
        prazointerno=data.get('prazointerno'),
        prazoexterno=data.get('prazoexterno'),
        entrega=data.get('entrega'),
        mensal=data.get('mensal'),
        responsavel=data.get('responsavel'),
        observacao=data.get('observacao')
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
    ordem.id_negocio = data.get('id_negocio', ordem.id_negocio)
    ordem.indicacao = data.get('indicacao', ordem.indicacao)
    ordem.agencia = data.get('agencia', ordem.agencia)
    ordem.id_produto = data.get('id_produto', ordem.id_produto)
    ordem.prazointerno = data.get('prazointerno', ordem.prazointerno)
    ordem.prazoexterno = data.get('prazoexterno', ordem.prazoexterno)
    ordem.entrega = data.get('entrega', ordem.entrega)
    ordem.mensal = data.get('mensal', ordem.mensal)
    ordem.responsavel = data.get('responsavel', ordem.responsavel)
    ordem.observacao = data.get('observacao', ordem.observacao)

    db.session.commit()
    return jsonify(ordem.serialize())

@ordens_de_servico_bp.route('/<int:id>', methods=['DELETE'])
def delete_ordem_de_servico(id):
    ordem = OrdemDeServico.query.get_or_404(id)
    db.session.delete(ordem)
    db.session.commit()
    return '', 204

@ordens_de_servico_bp.route('/usuario/<int:usuario_id>', methods=['GET'])
def get_ordens_de_servico_by_usuario(usuario_id):
    """Retorna todas as ordens de serviço de um usuário específico."""
    ordens = OrdemDeServico.query.filter_by(usuario_id=usuario_id).all()
    return jsonify([ordem.serialize() for ordem in ordens])