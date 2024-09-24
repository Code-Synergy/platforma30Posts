import requests
from flask import Blueprint, request, jsonify
from sqlalchemy import desc

from models.formulario_cliente import FormularioCliente
from models.ordens_de_servico import OrdemDeServico
from utils.token_verify import token_required
from . import db
from .clientes import consultaTele

legendas_bp = Blueprint('legendas', __name__)


class Legenda(db.Model):
    __tablename__ = 'legendas'

    id_legenda = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_form = db.Column(db.Integer, nullable=False)
    dia_post = db.Column(db.Integer, nullable=False)
    ds_legenda = db.Column(db.Text, nullable=False)
    img_legenda = db.Column(db.Text, nullable=True)
    bl_aprovado = db.Column(db.Boolean, default=False, nullable=True)
    bl_revisar = db.Column(db.Boolean, default=False, nullable=True)
    ds_revisao = db.Column(db.Text, nullable=True)
    bl_planner = db.Column(db.Boolean, default=False, nullable=True)
    ds_headline = db.Column(db.Text, nullable=False)
    ds_hashtag = db.Column(db.Text, nullable=False)

    def __init__(self, id_form, dia_post, ds_legenda, img_legenda=None, bl_aprovado=False, bl_revisar=False,
                 ds_revisao=None, bl_planner=False, ds_headline=None, ds_hashtag=None):
        self.id_form = id_form
        self.dia_post = dia_post
        self.ds_legenda = ds_legenda
        self.img_legenda = img_legenda
        self.bl_aprovado = bl_aprovado
        self.bl_revisar = bl_revisar
        self.ds_revisao = ds_revisao
        self.bl_planner = bl_planner
        self.ds_headline = ds_headline
        self.ds_hashtag = ds_hashtag

    def serialize(self):
        return {
            'id_legenda': self.id_legenda,
            'id_form': self.id_form,
            'dia_post': self.dia_post,
            'ds_legenda': self.ds_legenda,
            'img_legenda': self.img_legenda,
            'bl_aprovado': self.bl_aprovado,
            'bl_revisar': self.bl_revisar,
            'ds_revisao': self.ds_revisao,
            'bl_planner': self.bl_planner,
            'ds_headline': self.ds_headline,
            'ds_hashtag': self.ds_hashtag
        }


# Listar todas as legendas
@legendas_bp.route('/all', methods=['GET'])
def get_legendas_all():
    legendas = Legenda.query.all()
    return jsonify([l.serialize() for l in legendas])


@legendas_bp.route('/', methods=['GET'])
@token_required
def get_legendas(token_data):
    usuario_id = token_data.get('user_id')
    print('************************************************')
    print('USUÁRIO DO FORM é: ' + str(usuario_id))
    print('************************************************')
    # Buscar o formulário mais recente associado ao usuário
    ultimo_formulario = (FormularioCliente.query
                         .join(OrdemDeServico, FormularioCliente.ordem_id == OrdemDeServico.ordem_id)
                         .filter(OrdemDeServico.usuario_id == usuario_id)
                         .order_by(desc(FormularioCliente.updated_at))
                         .first())

    if not ultimo_formulario:
        return jsonify({"error": "Nenhum formulário encontrado para esse usuário"}), 404

    print('************************************************')
    print('FORM é: ' + str(ultimo_formulario.id_form))
    print('************************************************')
    # Buscar as legendas associadas ao último formulário
    legendas = (Legenda.query
                .filter_by(id_form=ultimo_formulario.id_form)
                .all())

    return jsonify([l.serialize() for l in legendas])


# Adicionar nova legenda
@legendas_bp.route('/', methods=['POST'])
def add_legenda():
    # Recebendo os dados da requisição diretamente
    data = request.get_json()
    return Legenda(data)


def geraLegenda(data):
    # Criando a instância da legenda com os dados recebidos
    print(data)
    legenda = Legenda(
        id_form=data.get('id_form'),
        dia_post=data.get('dia_post'),
        ds_legenda=data.get('ds_legenda'),
        img_legenda=data.get('img_legenda', None),
        bl_aprovado=data.get('bl_aprovado', False),
        bl_revisar=data.get('bl_revisar', False),
        ds_revisao=data.get('ds_revisao', None),
        bl_planner=data.get('bl_planner', False),
        ds_headline=data.get('ds_headline', None),
        ds_hashtag=data.get('ds_hashtag', None)
    )

    try:
        print('***********************************************')
        form_cliente = legenda.id_form
        print(form_cliente)
        # Adiciona e confirma a transação no banco de dados
        db.session.add(legenda)
        db.session.commit()
        print('***********************************************')
        print('COMITOU A LEGENDA')
        print('***********************************************')

        print('BORA AVISAR CLIENTE: ....')
        print("ENVIAR MENSAGEM NO WHATS.....")
        telefone = consultaTele(form_cliente)
        URLTigor = "https://tigor.itlabs.app/wpp/api"
        payload = {
            "app": "3bd82d2e-3077-4226-a366-1338eb3ed589",
            "number": telefone,
            "message": "Parabens! Seu post esta em produção.\n Obrigado por escolher a 30 Posts. \n Após apreciar seu post grátis o que acha de conhecer nossos planos ?",
            "type": "text",
            "url": ""
        }

        headers = {
            "Content-Type": "application/json"  # Define que o conteúdo enviado é JSON
        }

        responseWhats = requests.post(URLTigor, json=payload, headers=headers)

        if responseWhats.status_code == 200 or responseWhats.status_code == 201:
            print('Cliente informado com sucesso!')
        else:
            print('Erro ao informar cliente:')
            print(responseWhats.text)

        # Retorna a legenda adicionada com sucesso
        return jsonify(legenda.serialize()), 201
    except Exception as e:
        # Reverte a transação em caso de erro
        db.session.rollback()
        print(e)
        return jsonify({"error": "Erro ao adicionar legenda", "details": str(e)}), 400


# Atualizar legenda existente
@legendas_bp.route('/<int:id_legenda>', methods=['PUT'])
def update_legenda(id_legenda):
    legenda = Legenda.query.get_or_404(id_legenda)
    data = request.get_json()

    legenda.id_form = data.get('id_form', legenda.id_form)
    legenda.dia_post = data.get('dia_post', legenda.dia_post)
    legenda.ds_legenda = data.get('ds_legenda', legenda.ds_legenda)
    legenda.img_legenda = data.get('img_legenda', legenda.img_legenda)
    legenda.bl_aprovado = data.get('bl_aprovado', legenda.bl_aprovado)
    legenda.bl_revisar = data.get('bl_revisar', legenda.bl_revisar)
    legenda.ds_revisao = data.get('ds_revisao', legenda.ds_revisao)
    legenda.bl_planner = data.get('bl_planner', legenda.bl_planner)
    legenda.ds_headline = data.get('ds_headline', legenda.ds_headline)
    legenda.ds_hashtag = data.get('ds_hashtag', legenda.ds_hashtag)

    db.session.commit()
    return jsonify(legenda.serialize())


# Deletar legenda
@legendas_bp.route('/<int:id_legenda>', methods=['DELETE'])
def delete_legenda(id_legenda):
    legenda = Legenda.query.get_or_404(id_legenda)
    db.session.delete(legenda)
    db.session.commit()
    return '', 204
