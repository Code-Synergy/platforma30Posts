from flask import Blueprint, request, jsonify
from . import db

tipo_de_cliente_bp = Blueprint('tipo_cliente', __name__)

class TipoCliente(db.Model):
    __tablename__ = 'tipo_cliente'

    tipo_cliente_id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(255), nullable=False)

    def __init__(self, descricao):
        self.descricao = descricao

@tipo_de_cliente_bp.route('/', methods=['GET'])
def get_tipos_de_cliente():
    tipos = TipoCliente.query.all()
    return jsonify([t.serialize() for t in tipos])

@tipo_de_cliente_bp.route('/', methods=['POST'])
def add_tipo_de_cliente():
    data = request.get_json()
    tipo = TipoCliente(descricao=data['descricao'])
    db.session.add(tipo)
    db.session.commit()
    return jsonify(tipo.serialize()), 201

@tipo_de_cliente_bp.route('/<int:id>', methods=['PUT'])
def update_tipo_de_cliente(id):
    tipo = TipoCliente.query.get_or_404(id)
    data = request.get_json()

    tipo.descricao = data.get('descricao', tipo.descricao)

    db.session.commit()
    return jsonify(tipo.serialize())

@tipo_de_cliente_bp.route('/<int:id>', methods=['DELETE'])
def delete_tipo_de_cliente(id):
    tipo = TipoCliente.query.get_or_404(id)
    db.session.delete(tipo)
    db.session.commit()
    return '', 204
