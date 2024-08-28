from flask import Blueprint, request, jsonify
from models.formulario_cliente import FormularioCliente
from models.ordens_de_servico import OrdemDeServico
from utils.token_verify import token_required  
from marshmallow import Schema, fields, ValidationError
from . import db

class ClienteSchema(Schema):
    nome_cliente = fields.Str(required=True)
    whatsapp_cliente = fields.Str(required=True)
    email_cliente = fields.Email(required=True)
    nome_negocio = fields.Str(required=True)
    nicho = fields.Str(required=True)
    resumo_cliente = fields.Str(required=True)
    comeco = fields.Str(required=True)
    temas = fields.Str(required=True)
    produto = fields.Str(required=True)
    identidade_visual_1 = fields.Str(required=True)
    identidade_visual_2 = fields.Str(required=True)
    estilo = fields.Str(required=True)

    whatsapp_negocio = fields.Str()
    site = fields.Str()
    perfis_redes_sociais_1 = fields.Str()
    perfis_redes_sociais_2 = fields.Str()
    perfis_redes_sociais_3 = fields.Str()
    identidade_visual_3 = fields.Str()
    url_logo = fields.Str()
    comentarios = fields.Str()
    url_imagem_01 = fields.Str()
    url_imagem_02 = fields.Str()
    url_imagem_03 = fields.Str()
    url_imagem_04 = fields.Str()
    url_imagem_05 = fields.Str()
    url_imagem_06 = fields.Str()
    url_imagem_07 = fields.Str()
    url_imagem_08 = fields.Str()
    url_imagem_09 = fields.Str()
    url_imagem_10 = fields.Str()
    url_imagem_11 = fields.Str()
    url_imagem_12 = fields.Str()
    url_imagem_13 = fields.Str()
    url_imagem_14 = fields.Str()
    url_imagem_15 = fields.Str()
    url_imagem_16 = fields.Str()
    url_imagem_17 = fields.Str()
    url_imagem_18 = fields.Str()
    url_imagem_19 = fields.Str()
    url_imagem_20 = fields.Str()
    url_imagem_21 = fields.Str()
    url_imagem_22 = fields.Str()
    url_imagem_23 = fields.Str()
    url_imagem_24 = fields.Str()
    url_imagem_25 = fields.Str()
    url_imagem_26 = fields.Str()
    url_imagem_27 = fields.Str()
    url_imagem_28 = fields.Str()
    url_imagem_29 = fields.Str()
    url_imagem_30 = fields.Str()

form_bp = Blueprint('form', __name__)

cliente_schema = ClienteSchema()

@form_bp.route('/', methods=['POST'])
@token_required
def send_form(token_data):
    try:
        data = request.get_json()
        
        # Validação do body da requisição
        cliente_schema.load(data)

    except ValidationError as err:
        return jsonify(err.messages), 400
    
    form_id = token_data.get('id')
    
    # Verificando se o form_id é válido
    formulario = FormularioCliente.query.get_or_404(form_id)
    os = OrdemDeServico.query.get(formulario.ordem_id)
    
    try:
        # Atualizando os campos do formulário
        formulario.nome_cliente = data.get('nome_cliente', formulario.nome_cliente ) 
        formulario.whatsapp_cliente = data.get('whatsapp_cliente', formulario.whatsapp_cliente ) 
        formulario.email_cliente = data.get('email_cliente', formulario.email_cliente )
        formulario.nome_negocio = data.get('nome_negocio', formulario.nome_negocio )
        formulario.whatsapp_negocio = data.get('whatsapp_negocio', formulario.whatsapp_negocio )
        formulario.nicho = data.get('nicho', formulario.nicho )
        formulario.site = data.get('site', formulario.site )
        formulario.perfis_redes_sociais_1 = data.get('perfis_redes_sociais_1', formulario.perfis_redes_sociais_1 )
        formulario.perfis_redes_sociais_2 = data.get('perfis_redes_sociais_2', formulario.perfis_redes_sociais_2 )
        formulario.perfis_redes_sociais_3 = data.get('perfis_redes_sociais_3', formulario.perfis_redes_sociais_3 )
        formulario.resumo_cliente = data.get('resumo_cliente', formulario.resumo_cliente ) 
        formulario.comeco = data.get('comeco', formulario.comeco ) 
        formulario.temas = data.get('temas', formulario.temas ) 
        formulario.produto = data.get('produto', formulario.produto ) 
        formulario.identidade_visual_1 = data.get('identidade_visual_1', formulario.identidade_visual_1 )
        formulario.identidade_visual_2 = data.get('identidade_visual_2', formulario.identidade_visual_2 )
        formulario.identidade_visual_3 = data.get('identidade_visual_3', formulario.identidade_visual_3 )
        formulario.url_logo = data.get('url_logo', formulario.url_logo )
        formulario.estilo = data.get('estilo', formulario.estilo ) 
        formulario.comentarios = data.get('comentarios', formulario.comentarios ) 
        formulario.url_imagem_01 = data.get('url_imagem_01', formulario.url_imagem_01 )
        formulario.url_imagem_02 = data.get('url_imagem_02', formulario.url_imagem_02 )
        formulario.url_imagem_03 = data.get('url_imagem_03', formulario.url_imagem_03 )
        formulario.url_imagem_04 = data.get('url_imagem_04', formulario.url_imagem_04 )
        formulario.url_imagem_05 = data.get('url_imagem_05', formulario.url_imagem_05 )
        formulario.url_imagem_06 = data.get('url_imagem_06', formulario.url_imagem_06 )
        formulario.url_imagem_07 = data.get('url_imagem_07', formulario.url_imagem_07 )
        formulario.url_imagem_08 = data.get('url_imagem_08', formulario.url_imagem_08 )
        formulario.url_imagem_09 = data.get('url_imagem_09', formulario.url_imagem_09 )
        formulario.url_imagem_10 = data.get('url_imagem_10', formulario.url_imagem_10 )
        formulario.url_imagem_11 = data.get('url_imagem_11', formulario.url_imagem_11 )
        formulario.url_imagem_12 = data.get('url_imagem_12', formulario.url_imagem_12 )
        formulario.url_imagem_13 = data.get('url_imagem_13', formulario.url_imagem_13 )
        formulario.url_imagem_14 = data.get('url_imagem_14', formulario.url_imagem_14 )
        formulario.url_imagem_15 = data.get('url_imagem_15', formulario.url_imagem_15 )
        formulario.url_imagem_16 = data.get('url_imagem_16', formulario.url_imagem_16 )
        formulario.url_imagem_17 = data.get('url_imagem_17', formulario.url_imagem_17 )
        formulario.url_imagem_18 = data.get('url_imagem_18', formulario.url_imagem_18 )
        formulario.url_imagem_19 = data.get('url_imagem_19', formulario.url_imagem_19 )
        formulario.url_imagem_20 = data.get('url_imagem_20', formulario.url_imagem_20 )
        formulario.url_imagem_21 = data.get('url_imagem_21', formulario.url_imagem_21 )
        formulario.url_imagem_22 = data.get('url_imagem_22', formulario.url_imagem_22 )
        formulario.url_imagem_23 = data.get('url_imagem_23', formulario.url_imagem_23 )
        formulario.url_imagem_24 = data.get('url_imagem_24', formulario.url_imagem_24 )
        formulario.url_imagem_25 = data.get('url_imagem_25', formulario.url_imagem_25 )
        formulario.url_imagem_26 = data.get('url_imagem_26', formulario.url_imagem_26 )
        formulario.url_imagem_27 = data.get('url_imagem_27', formulario.url_imagem_27 )
        formulario.url_imagem_28 = data.get('url_imagem_28', formulario.url_imagem_28 )
        formulario.url_imagem_29 = data.get('url_imagem_29', formulario.url_imagem_29 )
        formulario.url_imagem_30 = data.get('url_imagem_30', formulario.url_imagem_30 )
        
        os.workflow_id = 2

        db.session.commit()

        return jsonify({}), 204

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500