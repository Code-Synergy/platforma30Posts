from flask import Blueprint, request, jsonify
from . import db

formulario_cliente_bp = Blueprint('formulario_cliente', __name__)

class FormularioCliente(db.Model):
    __tablename__ = 'formulario_cliente'

    form_id = db.Column(db.Integer, primary_key=True)
    os_id = db.Column(db.Integer, db.ForeignKey('ordens_de_servico.os_id'))
    nome = db.Column(db.String(255))
    whatsapp = db.Column(db.String(20))
    email = db.Column(db.String(255))
    negocio = db.Column(db.String(255))
    whatsapp_negocio = db.Column(db.String(20))
    nicho = db.Column(db.String(255))
    site = db.Column(db.String(255))
    perfil_rede_social_1 = db.Column(db.String(255))
    perfil_rede_social_2 = db.Column(db.String(255))
    perfil_rede_social_3 = db.Column(db.String(255))
    resumo = db.Column(db.Text)
    comeco = db.Column(db.Text)
    temas = db.Column(db.Text)
    produto = db.Column(db.Text)
    identidade_visual_1 = db.Column(db.String(255))
    identidade_visual_2 = db.Column(db.String(255))
    identidade_visual_3 = db.Column(db.String(255))
    url_logo = db.Column(db.String(255))
    estilo = db.Column(db.String(255))
    url_imagens = db.Column(db.String(255))
    comentarios = db.Column(db.Text)
    workflow_id = db.Column(db.Integer, db.ForeignKey('workflow.workflow_id'))

    def __init__(self, os_id, nome, whatsapp, email, negocio, whatsapp_negocio, nicho, site, perfil_rede_social_1, perfil_rede_social_2, perfil_rede_social_3, resumo, comeco, temas, produto, identidade_visual_1, identidade_visual_2, identidade_visual_3, url_logo, estilo, url_imagens, comentarios, workflow_id):
        self.os_id = os_id
        self.nome = nome
        self.whatsapp = whatsapp
        self.email = email
        self.negocio = negocio
        self.whatsapp_negocio = whatsapp_negocio
        self.nicho = nicho
        self.site = site
        self.perfil_rede_social_1 = perfil_rede_social_1
        self.perfil_rede_social_2 = perfil_rede_social_2
        self.perfil_rede_social_3 = perfil_rede_social_3
        self.resumo = resumo
        self.comeco = comeco
        self.temas = temas
        self.produto = produto
        self.identidade_visual_1 = identidade_visual_1
        self.identidade_visual_2 = identidade_visual_2
        self.identidade_visual_3 = identidade_visual_3
        self.url_logo = url_logo
        self.estilo = estilo
        self.url_imagens = url_imagens
        self.comentarios = comentarios
        self.workflow_id = workflow_id

@formulario_cliente_bp.route('/', methods=['GET'])
def get_formularios_cliente():
    formularios = FormularioCliente.query.all()
    return jsonify([f.serialize() for f in formularios])

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
