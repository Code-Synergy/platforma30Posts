from flask import Blueprint, request, jsonify
from . import db

negocios_bp = Blueprint('negocios', __name__)

class Negocio(db.Model):
    __tablename__ = 'negocios'

    negocio_id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, nullable=False)
    nome_negocio = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text)
    ativo = db.Column(db.Boolean, default=True)

    def __init__(self, cliente_id, nome_negocio, descricao=None, ativo=True):
        self.cliente_id = cliente_id
        self.nome_negocio = nome_negocio
        self.descricao = descricao
        self.ativo = ativo

    def serialize(self):
        return {
            'negocio_id': self.negocio_id,
            'cliente_id': self.cliente_id,
            'nome_negocio': self.nome_negocio,
            'descricao': self.descricao,
            'ativo': self.ativo
        }

@negocios_bp.route('/', methods=['GET'])
def get_negocios():
    """Retorna todos os negócios"""
    negocios = Negocio.query.all()
    return jsonify([n.serialize() for n in negocios])

@negocios_bp.route('/cliente/<int:cliente_id>', methods=['GET'])
def get_negocios_by_cliente(cliente_id):
    """Retorna todos os negócios de um cliente específico"""
    negocios = Negocio.query.filter_by(cliente_id=cliente_id).all()
    return jsonify([n.serialize() for n in negocios])

@negocios_bp.route('/<int:id>', methods=['GET'])
def get_negocio_by_id(id):
    """Retorna um negócio específico pelo ID"""
    negocio = Negocio.query.get_or_404(id)
    return jsonify(negocio.serialize())

@negocios_bp.route('/', methods=['POST'])
def add_negocio():
    """Adiciona um novo negócio"""
    data = request.get_json()
    negocio = Negocio(
        cliente_id=data['cliente_id'],
        nome_negocio=data['nome_negocio'],
        descricao=data.get('descricao'),
        ativo=data.get('ativo', True)
    )
    db.session.add(negocio)
    db.session.commit()
    return jsonify(negocio.serialize()), 201

@negocios_bp.route('/<int:id>', methods=['PUT'])
def update_negocio(id):
    """Atualiza um negócio existente"""
    negocio = Negocio.query.get_or_404(id)
    data = request.get_json()

    negocio.cliente_id = data.get('cliente_id', negocio.cliente_id)
    negocio.nome_negocio = data.get('nome_negocio', negocio.nome_negocio)
    negocio.descricao = data.get('descricao', negocio.descricao)
    negocio.ativo = data.get('ativo', negocio.ativo)

    db.session.commit()
    return jsonify(negocio.serialize())

@negocios_bp.route('/<int:id>', methods=['DELETE'])
def delete_negocio(id):
    """Remove um negócio"""
    negocio = Negocio.query.get_or_404(id)
    db.session.delete(negocio)
    db.session.commit()
    return '', 204
