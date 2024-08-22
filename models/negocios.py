from flask import Blueprint, request, jsonify
from . import db

negocios_bp = Blueprint('negocios', __name__)


class Negocio(db.Model):
    __tablename__ = 'negocios'

    negocio_id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.cliente_id'))
    nome_negocio = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text)

    def __init__(self, cliente_id, nome_negocio, descricao=None):
        self.cliente_id = cliente_id
        self.nome_negocio = nome_negocio
        self.descricao = descricao


@negocios_bp.route('/', methods=['GET'])
def get_negocios():
    negocios = Negocio.query.all()
    return jsonify([n.serialize() for n in negocios])

@negocios_bp.route('/', methods=['POST'])
def add_negocio():
    data = request.get_json()
    negocio = Negocio(
        cliente_id=data['cliente_id'],
        nome_negocio=data['nome_negocio'],
        descricao=data.get('descricao')
    )
    db.session.add(negocio)
    db.session.commit()
    return jsonify(negocio.serialize()), 201

@negocios_bp.route('/<int:id>', methods=['PUT'])
def update_negocio(id):
    negocio = Negocio.query.get_or_404(id)
    data = request.get_json()

    negocio.nome_negocio = data.get('nome_negocio', negocio.nome_negocio)
    negocio.descricao = data.get('descricao', negocio.descricao)

    db.session.commit()
    return jsonify(negocio.serialize())

@negocios_bp.route('/<int:id>', methods=['DELETE'])
def delete_negocio(id):
    negocio = Negocio.query.get_or_404(id)
    db.session.delete(negocio)
    db.session.commit()
    return '', 204
