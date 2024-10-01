from flask import Blueprint, jsonify, request
import datetime

from models import db
from models.clientes import Cliente
from models.formulario_cliente import FormularioCliente
from models.negocios import Negocio
from models.ordens_de_servico import OrdemDeServico
from models.pedido import Pedido
from models.user import Usuarios
from utils.token_verify import token_required
import uuid

orquestra_bp = Blueprint('orquestra', __name__)


@orquestra_bp.route('/<int:id_produto>', methods=['POST'])
@token_required
def GeraPedido(token_data, id_produto):
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
        nome_negocio='',
        descricao='',
        ativo=True
    )
    db.session.add(negocio)
    db.session.commit()

    # Adiciona o pedido
    if id_produto != 1:
        descricao = 'Premium'
    else:
        descricao = 'Post Free'

    pedido = Pedido(
        negocio_id=negocio.negocio_id,
        descricao=descricao,
        valor=0,
        cliente_id=user_id,  # Incluindo cliente_id
        ativo=True  # Incluindo ativo
    )
    db.session.add(pedido)
    db.session.commit()

    # Adiciona Ordem de serviço
    ordem = OrdemDeServico(
        pedido_id=pedido.pedido_id,
        descricao=descricao,
        data=datetime.datetime.now(),  # Usando a data corretamente
        usuario_id=user_id,
        workflow_id=1,
        id_negocio=negocio.negocio_id,
        id_produto=id_produto,
        prazointerno=datetime.datetime.now(),  # Usando a data corretamente
        prazoexterno=datetime.datetime.now(),  # Usando a data corretamente
        entrega=datetime.datetime.now(),  # Usando a data corretamente
        mensal=False,
    )
    db.session.add(ordem)
    db.session.commit()
    id_form = uuid.uuid4()
    # Adiciona o Formulário para preenchimento
    formulario = FormularioCliente(
        id_form=id_form,
        ordem_id=ordem.ordem_id,
        nome_cliente='',
        whatsapp_cliente='',
        email_cliente=user.email,
        #TODO Ajustar para lógico de balanceamento de SM
        id_usuarioSocialMedia=3
    )
    db.session.add(formulario)
    db.session.commit()

    return jsonify({'FormID': id_form}), 201
