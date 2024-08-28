from flask import Blueprint, request, jsonify
from . import db

pedidos_bp = Blueprint('pedidos', __name__)

class Pedido(db.Model):
    __tablename__ = 'pedidos'

    pedido_id = db.Column(db.Integer, primary_key=True)
    negocio_id = db.Column(db.Integer, nullable=False)
    descricao = db.Column(db.Text)
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    cliente_id = db.Column(db.Integer)  # Incluindo cliente_id
    ativo = db.Column(db.Boolean, default=True)  # Incluindo ativo

    def serialize(self):
        return {
            'pedido_id': self.pedido_id,
            'negocio_id': self.negocio_id,
            'descricao': self.descricao,
            'valor': str(self.valor),  # Converter para string para evitar problemas de serialização
            'cliente_id': self.cliente_id,
            'ativo': self.ativo
        }

# Listar todos os pedidos
@pedidos_bp.route('/', methods=['GET'])
def get_pedidos():
    """Retorna todos os pedidos"""
    pedidos = Pedido.query.all()
    return jsonify([p.serialize() for p in pedidos])

# Listar pedidos por cliente_id
@pedidos_bp.route('/cliente/<int:cliente_id>', methods=['GET'])
def get_pedidos_by_cliente(cliente_id):
    """Retorna todos os pedidos de um cliente específico"""
    pedidos = Pedido.query.filter_by(cliente_id=cliente_id).all()
    return jsonify([p.serialize() for p in pedidos])

# Incluir novo pedido
@pedidos_bp.route('/', methods=['POST'])
def add_pedido():
    data = request.get_json()
    pedido = Pedido(
        negocio_id=data['negocio_id'],
        descricao=data.get('descricao'),
        valor=data['valor'],
        cliente_id=data.get('cliente_id'),  # Incluindo cliente_id
        ativo=data.get('ativo', True)  # Incluindo ativo
    )
    db.session.add(pedido)
    db.session.commit()
    return jsonify(pedido.serialize()), 201



# Alterar pedido existente
@pedidos_bp.route('/<int:pedido_id>', methods=['PUT'])
def update_pedido(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    data = request.get_json()

    pedido.cliente_id = data.get('cliente_id', pedido.cliente_id)
    pedido.descricao = data.get('descricao', pedido.descricao)
    pedido.ativo = data.get('ativo', pedido.ativo)

    db.session.commit()
    return jsonify(pedido.serialize())

# Deletar pedido existente
@pedidos_bp.route('/<int:pedido_id>', methods=['DELETE'])
def delete_pedido(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    db.session.delete(pedido)
    db.session.commit()
    return '', 204
