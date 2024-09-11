from flask import Blueprint, request, jsonify
from . import db

clientes_bp = Blueprint('clientes', __name__)


class Cliente(db.Model):
    __tablename__ = 'clientes'

    cliente_id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    contato = db.Column(db.String(255))
    segmento = db.Column(db.String(255))
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(255))
    pais = db.Column(db.String(100))
    tipo_cliente_id = db.Column(db.Integer, db.ForeignKey('tipo_cliente.tipo_cliente_id'))
    ativo = db.Column(db.Boolean, default=True)

    def __init__(self, nome, contato, segmento, telefone, email, pais, tipo_cliente_id, ativo=True):
        self.nome = nome
        self.contato = contato
        self.segmento = segmento
        self.telefone = telefone
        self.email = email
        self.pais = pais
        self.tipo_cliente_id = tipo_cliente_id
        self.ativo = ativo

    def serialize(self):
        return {
            'cliente_id': self.cliente_id,
            'nome': self.nome,
            'contato': self.contato,
            'segmento': self.segmento,
            'telefone': self.telefone,
            'email': self.email,
            'pais': self.pais,
            'tipo_cliente_id': self.tipo_cliente_id,
            'ativo': self.ativo
        }


@clientes_bp.route('/', methods=['GET'])
def get_clientes():
    clientes = Cliente.query.all()
    return jsonify([c.serialize() for c in clientes])


@clientes_bp.route('/search', methods=['GET'])
def search_clientes():
    nome = request.args.get('nome', '')

    # Pesquisa por clientes cujo nome contém a string fornecida (case-insensitive)
    clientes = Cliente.query.filter(Cliente.nome.ilike(f'%{nome}%')).all()

    return jsonify([c.serialize() for c in clientes])


@clientes_bp.route('/LoginSearch', methods=['GET'])
def search_clientesbyemail():
    email = request.args.get('email', '')

    # Pesquisa por clientes cujo nome contém a string fornecida (case-insensitive)
    clientes = Cliente.query.filter(Cliente.nome.ilike(f'%{email}%')).all()

    return jsonify([c.serialize() for c in clientes])


@clientes_bp.route('/', methods=['POST'])
def add_cliente():
    data = request.get_json()
    cliente = Cliente(
        nome=data['nome'],
        contato=data.get('contato'),
        segmento=data.get('segmento'),
        telefone=data.get('telefone'),
        email=data.get('email'),
        pais=data.get('pais'),
        tipo_cliente_id=data.get('tipo_cliente_id'),
        ativo=data.get('ativo', True)
    )
    db.session.add(cliente)

    db.session.commit()

    return jsonify(cliente.serialize()), 201


@clientes_bp.route('/<int:id>', methods=['PUT'])
def update_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    data = request.get_json()

    cliente.nome = data.get('nome', cliente.nome)
    cliente.contato = data.get('contato', cliente.contato)
    cliente.segmento = data.get('segmento', cliente.segmento)
    cliente.telefone = data.get('telefone', cliente.telefone)
    cliente.email = data.get('email', cliente.email)
    cliente.pais = data.get('pais', cliente.pais)
    cliente.tipo_cliente_id = data.get('tipo_cliente_id', cliente.tipo_cliente_id)
    cliente.ativo = data.get('ativo', cliente.ativo)

    db.session.commit()
    return jsonify(cliente.serialize())


@clientes_bp.route('/<int:id>', methods=['DELETE'])
def delete_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    return '', 204
