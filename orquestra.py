from flask import Blueprint, request, jsonify, current_app
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

from models import db
from models.formulario_cliente import FormularioCliente
from models.negocios import Negocio
from models.ordens_de_servico import OrdemDeServico
from models.pedido import pedidos_bp, Pedido
from models.send_form import cliente_schema
from utils.token_verify import token_required

orquestra_bp = Blueprint('orquestra', __name__)

@orquestra_bp.route('/', methods=['POST'])
@token_required
def GeraPedido(token_data):

    try:
        data = request.get_json()

        # Validação do body da requisição
        cliente_schema.load(data)

    except ValidationError as err:
        return jsonify(err.messages), 400

    user_id = token_data.get('user_id')

    #Adicona um negócio
    negocio = Negocio(
        cliente_id=user_id,
        nome_negocio='batata',
        descricao='batata',
        ativo=True
    )
    db.session.add(negocio)

    #Adiciona o pedido
    data = request.get_json()
    pedido = Pedido(
        negocio_id=negocio.negocio_id,
        descricao='Post Free',
        valor=0,
        cliente_id=user_id,  # Incluindo cliente_id
        ativo=True  # Incluindo ativo
    )
    db.session.add(pedido)

    #Adiciona Ordem de serviço
    ordem = OrdemDeServico(
        pedido_id=pedido.pedido_id,
        descricao='Post Free',
        data=datetime,
        usuario_id=user_id,
        workflow_id=1,
        id_form='',
        id_negocio=negocio.negocio_id,
        indicacao='',
        agencia='',
        id_produto=1,
        prazointerno=datetime,
        prazoexterno=datetime,
        entrega=datetime,
        mensal='',
        responsavel='ZOE',
        observacao=''
    )
    db.session.add(ordem)

    #Adiciona o Formulário para preechimento
    formulario = FormularioCliente(
        os_id=ordem.ordem_id,
        whatsapp='',
        email='email'
    )
    db.session.add(formulario)

    db.session.commit()

    return jsonify({'FormID': formulario.id_form}), 201

