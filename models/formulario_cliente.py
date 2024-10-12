from flask import Blueprint, request, jsonify
from sqlalchemy import DateTime, func
from . import db
from utils.token_verify import token_required
from . import db

formulario_cliente_bp = Blueprint('formulario_cliente', __name__)


class FormularioCliente(db.Model):
    __tablename__ = 'formulario_cliente'

    id_form = db.Column(db.String(36), primary_key=True, default=db.func.gen_random_uuid())
    ordem_id = db.Column(db.Integer)
    nome_cliente = db.Column(db.String(255))
    whatsapp_cliente = db.Column(db.String(20), nullable=False)
    email_cliente = db.Column(db.String(255), nullable=False)
    nome_negocio = db.Column(db.String(255))
    whatsapp_negocio = db.Column(db.String(20))
    nicho = db.Column(db.String(255))
    site = db.Column(db.String(255))
    perfis_redes_sociais_1 = db.Column(db.String(255))
    perfis_redes_sociais_2 = db.Column(db.String(255))
    perfis_redes_sociais_3 = db.Column(db.String(255))
    resumo_cliente = db.Column(db.Text)
    comeco = db.Column(db.Text)
    temas = db.Column(db.Text)
    produto = db.Column(db.Text)
    identidade_visual_1 = db.Column(db.String(255))
    identidade_visual_2 = db.Column(db.String(255))
    identidade_visual_3 = db.Column(db.String(255))
    url_logo = db.Column(db.String(255))
    estilo = db.Column(db.Text)
    comentarios = db.Column(db.Text)

    url_imagem_01 = db.Column(db.String(255))
    url_imagem_02 = db.Column(db.String(255))
    url_imagem_03 = db.Column(db.String(255))
    url_imagem_04 = db.Column(db.String(255))
    url_imagem_05 = db.Column(db.String(255))
    url_imagem_06 = db.Column(db.String(255))
    url_imagem_07 = db.Column(db.String(255))
    url_imagem_08 = db.Column(db.String(255))
    url_imagem_09 = db.Column(db.String(255))
    url_imagem_10 = db.Column(db.String(255))
    url_imagem_11 = db.Column(db.String(255))
    url_imagem_12 = db.Column(db.String(255))
    url_imagem_13 = db.Column(db.String(255))
    url_imagem_14 = db.Column(db.String(255))
    url_imagem_15 = db.Column(db.String(255))
    url_imagem_16 = db.Column(db.String(255))
    url_imagem_17 = db.Column(db.String(255))
    url_imagem_18 = db.Column(db.String(255))
    url_imagem_19 = db.Column(db.String(255))
    url_imagem_20 = db.Column(db.String(255))
    url_imagem_21 = db.Column(db.String(255))
    url_imagem_22 = db.Column(db.String(255))
    url_imagem_23 = db.Column(db.String(255))
    url_imagem_24 = db.Column(db.String(255))
    url_imagem_25 = db.Column(db.String(255))
    url_imagem_26 = db.Column(db.String(255))
    url_imagem_27 = db.Column(db.String(255))
    url_imagem_28 = db.Column(db.String(255))
    url_imagem_29 = db.Column(db.String(255))
    url_imagem_30 = db.Column(db.String(255))
    created_at = db.Column(DateTime, default=func.now())
    updated_at = db.Column(DateTime, default=func.now(), onupdate=func.now())

    def __init__(self, id_form, ordem_id, nome_cliente, whatsapp_cliente, email_cliente, nome_negocio=None,
                 whatsapp_negocio=None,
                 nicho=None, site=None, perfis_redes_sociais_1=None, perfis_redes_sociais_2=None,
                 perfis_redes_sociais_3=None,
                 resumo_cliente=None, comeco=None, temas=None, produto=None, identidade_visual_1=None,
                 identidade_visual_2=None,
                 identidade_visual_3=None, url_logo=None, estilo=None, comentarios=None, **kwargs):
        self.id_form = id_form
        self.ordem_id = ordem_id
        self.nome_cliente = nome_cliente
        self.whatsapp_cliente = whatsapp_cliente
        self.email_cliente = email_cliente
        self.nome_negocio = nome_negocio
        self.whatsapp_negocio = whatsapp_negocio
        self.nicho = nicho
        self.site = site
        self.perfis_redes_sociais_1 = perfis_redes_sociais_1
        self.perfis_redes_sociais_2 = perfis_redes_sociais_2
        self.perfis_redes_sociais_3 = perfis_redes_sociais_3
        self.resumo_cliente = resumo_cliente
        self.comeco = comeco
        self.temas = temas
        self.produto = produto
        self.identidade_visual_1 = identidade_visual_1
        self.identidade_visual_2 = identidade_visual_2
        self.identidade_visual_3 = identidade_visual_3
        self.url_logo = url_logo
        self.estilo = estilo
        self.comentarios = comentarios

        # Atribuir URLs das imagens (até 30)
        for i in range(1, 31):
            setattr(self, f'url_imagem_{i:02}', kwargs.get(f'url_imagem_{i:02}'))


@formulario_cliente_bp.route('/all', methods=['GET'])
def get_formularios_cliente():
    formularios = FormularioCliente.query.all()
    return jsonify([f.serialize() for f in formularios])


@formulario_cliente_bp.route('/', methods=['GET'])
@token_required
def get_formularios_cliente_id(token_data):
    form_id = token_data.get('id')
    formularios = FormularioCliente.query.get(form_id)
    if formularios:
        return jsonify({
            'telefone': formularios.whatsapp_cliente,
            'email': formularios.email_cliente
        })
    else:
        return jsonify({'message': 'Not Found!'}), 404


@formulario_cliente_bp.route('/', methods=['POST'])
def add_formulario_cliente():
    data = request.get_json()
    formulario = FormularioCliente(
        os_id=data['os_id'],
        nome=data.get('nome'),
        whatsapp=data.get('whatsapp'),
        email=data.get('email'),
        negocio=data.get('negocio'),
        whatsapp_negocio=data.get('whatsapp_negocio'),
        nicho=data.get('nicho'),
        site=data.get('site'),
        perfil_rede_social_1=data.get('perfil_rede_social_1'),
        perfil_rede_social_2=data.get('perfil_rede_social_2'),
        perfil_rede_social_3=data.get('perfil_rede_social_3'),
        resumo=data.get('resumo'),
        comeco=data.get('comeco'),
        temas=data.get('temas'),
        produto=data.get('produto'),
        identidade_visual_1=data.get('identidade_visual_1'),
        identidade_visual_2=data.get('identidade_visual_2'),
        identidade_visual_3=data.get('identidade_visual_3'),
        url_logo=data.get('url_logo'),
        estilo=data.get('estilo'),
        url_imagens=data.get('url_imagens'),
        comentarios=data.get('comentarios'),
        workflow_id=data.get('workflow_id')
    )
    db.session.add(formulario)
    db.session.commit()
    return jsonify(formulario.serialize()), 201


@formulario_cliente_bp.route('/<int:id>', methods=['PUT'])
def update_formulario_cliente(id):
    formulario = FormularioCliente.query.get_or_404(id)
    data = request.get_json()

    formulario.nome = data.get('nome', formulario.nome)
    formulario.whatsapp = data.get('whatsapp', formulario.whatsapp)
    formulario.email = data.get('email', formulario.email)
    formulario.negocio = data.get('negocio', formulario.negocio)
    formulario.whatsapp_negocio = data.get('whatsapp_negocio', formulario.whatsapp_negocio)
    formulario.nicho = data.get('nicho', formulario.nicho)
    formulario.site = data.get('site', formulario.site)
    formulario.perfil_rede_social_1 = data.get('perfil_rede_social_1', formulario.perfil_rede_social_1)
    formulario.perfil_rede_social_2 = data.get('perfil_rede_social_2', formulario.perfil_rede_social_2)
    formulario.perfil_rede_social_3 = data.get('perfil_rede_social_3', formulario.perfil_rede_social_3)
    formulario.resumo = data.get('resumo', formulario.resumo)
    formulario.comeco = data.get('comeco', formulario.comeco)
    formulario.temas = data.get('temas', formulario.temas)
    formulario.produto = data.get('produto', formulario.produto)
    formulario.identidade_visual_1 = data.get('identidade_visual_1', formulario.identidade_visual_1)
    formulario.identidade_visual_2 = data.get('identidade_visual_2', formulario.identidade_visual_2)
    formulario.identidade_visual_3 = data.get('identidade_visual_3', formulario.identidade_visual_3)
    formulario.url_logo = data.get('url_logo', formulario.url_logo)
    formulario.estilo = data.get('estilo', formulario.estilo)
    formulario.url_imagens = data.get('url_imagens', formulario.url_imagens)
    formulario.comentarios = data.get('comentarios', formulario.comentarios)
    formulario.workflow_id = data.get('workflow_id', formulario.workflow_id)

    db.session.commit()
    return jsonify(formulario.serialize())


@formulario_cliente_bp.route('/<int:id>', methods=['DELETE'])
def delete_formulario_cliente(id):
    formulario = FormularioCliente.query.get_or_404(id)
    db.session.delete(formulario)
    db.session.commit()
    return '', 204


def get_formularios_form_id(id_form):
    formularios = FormularioCliente.query.get(id_form)
    return formularios
