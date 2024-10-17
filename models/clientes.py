from flask import Blueprint, request, jsonify

from utils.token_verify import token_required
from . import db
from .formulario_cliente import FormularioCliente
from .ordens_de_servico import OrdemDeServico
from .user import Usuarios

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


@clientes_bp.route('/LoginSearch', methods=['POST'])
def search_clientesbyemail():
    data = request.get_json()
    email = data.get('email')
    # Pesquisa por clientes cujo nome contém a string fornecida (case-insensitive)
    clientes = Cliente.query.filter(Cliente.email.ilike(f'%{email}%')).all()

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

    Usuarios.query.update()
    Usuarios.query.filter_by(email=cliente.email).update({
            "img_user": data.get('img_user'),
            "username": data.get('nome')
            })
    db.session.commit()

    return jsonify(cliente.serialize())


@clientes_bp.route('/<int:id>', methods=['DELETE'])
def delete_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    return '', 204


def consultaTele(id_form):
    # Pesquisa por id do cliente e retornar o telefone
    print('CONSULTANTADO TELE....')
    #formularios = FormularioCliente.query.filter(FormularioCliente.id_form == id_form).first()
    result = FormularioCliente.query.with_entities(FormularioCliente.ordem_id,
                                                   FormularioCliente.whatsapp_cliente).filter(
        FormularioCliente.id_form == id_form).first()

    # Extrai os valores dos campos, caso não seja None
    ordem_id = result[0] if result else None
    whatsapp_cliente = result[1] if result else None
    print('Ordem ID: ' + str(ordem_id))
    print('WhatsAPP: ' + str(whatsapp_cliente))

    #ordens = OrdemDeServico.query.filter(OrdemDeServico.id == ordem_id).first()
    #id_cliente = ordens.get('usuario_id')
    #print('Buscou Cliente na Ordem: ' + id_cliente)

    #clientes = Cliente.query.filter(Cliente.cliente_id.ilike(id_cliente)).all()
    #telefone = clientes.get('telefone')
    #print('Pegou o telefone do cliente:' + telefone)
    return whatsapp_cliente




@clientes_bp.route('/updtPerson', methods=['PUT'])
@token_required
def update_cliente(token_data):
    user_id = token_data.get('user_id')
    data = request.get_json()
    Usuarios.query.update()
    Usuarios.query.filter_by(usuario_id=user_id).update({
        "img_user": data.get('img_user'),
        "username": data.get('nome')
    })
    db.session.commit()

    cliente = Cliente.query.get_or_404(id)
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
