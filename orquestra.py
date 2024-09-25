from flask import Blueprint, jsonify
import datetime

from models import db
from models.clientes import Cliente
from models.formulario_cliente import FormularioCliente
from models.negocios import Negocio
from models.ordens_de_servico import OrdemDeServico
from models.pedido import Pedido
from models.user import Usuarios
from utils.token_verify import token_required

orquestra_bp = Blueprint('orquestra', __name__)


@orquestra_bp.route('/', methods=['POST'])
@token_required
def GeraPedido(token_data):
    user_id = token_data.get('user_id')

    user = Usuarios.query.get_or_404(user_id)

    cliente = Cliente(
        nome=user.email,
        email=user.email,
        contato="",
        segmento="",
        telefone="",
        pais="",
        tipo_cliente_id=1
    )
    db.session.add(cliente)
    db.session.commit()

    # Adiciona um negócio
    negocio = Negocio(
        cliente_id=cliente.cliente_id,
        nome_negocio='batata',
        descricao='batata',
        ativo=True
    )
    db.session.add(negocio)
    db.session.commit()

    # Adiciona o pedido
    pedido = Pedido(
        negocio_id=negocio.negocio_id,
        descricao='Post Free',
        valor=0,
        cliente_id=user_id,  # Incluindo cliente_id
        ativo=True  # Incluindo ativo
    )
    db.session.add(pedido)
    db.session.commit()

    # Adiciona Ordem de serviço
    ordem = OrdemDeServico(
        pedido_id=pedido.pedido_id,
        descricao='Post Free',
        data=datetime.datetime.now(),  # Usando a data corretamente
        usuario_id=user_id,
        workflow_id=1,
        id_negocio=negocio.negocio_id,
        id_produto=1,
        prazointerno=datetime.datetime.now(),  # Usando a data corretamente
        prazoexterno=datetime.datetime.now(),  # Usando a data corretamente
        entrega=datetime.datetime.now(),  # Usando a data corretamente
        mensal=False,
    )
    db.session.add(ordem)
    db.session.commit()

    # Adiciona o Formulário para preenchimento
    formulario = FormularioCliente(
        ordem_id=ordem.ordem_id,
        nome_cliente='',
        whatsapp_cliente='',
        email_cliente=user.email
    )
    db.session.add(formulario)
    db.session.commit()

    return jsonify({'FormID': formulario.id_form}), 201
