import requests
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from . import db
from .Gepeto_Zoe_Fluxo1 import processar_legendas, validaFluxo
from .clientes import Cliente
import random
import string
from sqlalchemy.exc import IntegrityError
from .formulario_cliente import FormularioCliente, get_formularios_form_id
from .negocios import Negocio
from .ordens_de_servico import OrdemDeServico
from .pedido import Pedido
from datetime import datetime, timezone, timedelta
import uuid

# API de envio de mensagem Whats
URLTigor = "https://tigor.itlabs.app/wpp/api"
KEYTigor = "3bd82d2e-3077-4226-a366-1338eb3ed589"
headers_Tigor = {"Content-Type": "application/json"}

global password

# Definindo o modelo de perfis
class Perfis(db.Model):
    __tablename__ = 'perfis'

    perfil_id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), unique=True, nullable=False)


# Definindo o modelo de usuários
class Usuarios(db.Model):
    __tablename__ = 'usuarios'

    usuario_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    perfil_id = db.Column(db.Integer, db.ForeignKey('perfis.perfil_id'), nullable=True)

    # Relacionamento com a tabela Perfis
    perfil = db.relationship('Perfis', backref='usuarios')

    def serialize(self):
        return {
            'usuario_id': self.usuario_id,
            'username': self.username,
            'email': self.email,
            'perfil_nome': self.perfil.nome if self.perfil else 'Sem Perfil'  # Verifica se o perfil existe
        }


user_bp = Blueprint('user', __name__)


@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    perfil_id = data.get('perfil_id')

    # Use 'pbkdf2:sha256' para gerar o hash da senha
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    # Cria um novo usuário
    new_user = Usuarios(username=username, senha=hashed_password, email=email, perfil_id=perfil_id)

    try:
        db.session.add(new_user)
        db.session.commit()

        # INSERE CLIENTE
        try:
            # Insere o cliente na tabela
            cliente = Cliente(
                nome='',
                contato='',
                segmento='',
                telefone='',
                email=email,
                pais='',
                tipo_cliente_id=0,
                ativo=True
            )
            db.session.add(cliente)
            print('Vai inserir cliente')
            db.session.commit()
            print('Vai INSERIU FDP')

            return jsonify(cliente.serialize()), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = Usuarios.query.filter_by(email=email).first()

    if user and check_password_hash(user.senha, password):
        token = jwt.encode({
            'perfil': user.perfil_id,
            'user_id': user.usuario_id,
            'exp': datetime.now(timezone.utc) + timedelta(hours=1)
        }, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

        return jsonify({'token': token, 'perfil': user.perfil_id, 'email': user.email}), 200

    else:
        return jsonify({'message': 'Invalid credentials'}), 401


# Listar todos os usuários
@user_bp.route('/', methods=['GET'])
def get_user():
    """Retorna todos os usuários"""
    users = Usuarios.query.all()
    return jsonify([user.serialize() for user in users])


@user_bp.route('/registerWhats', methods=['POST'])
def registerWhats():

    # Cria um utilizador
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    telefone = data.get('telefone')
    perfil_id = 1

    try:
        #new_user SE EXISTE UM USUÁRIO
        new_user = Usuarios.query.filter_by(email=email).first()
        if new_user is None:
            # Use 'pbkdf2:sha256' para gerar o hash da senha
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = Usuarios(username=username, senha=hashed_password, email=email, perfil_id=perfil_id)
            print('VAI ADICIONAR')
            db.session.add(new_user)
            db.session.commit()
        else:
            print('CLIENTE EXISTENTE .....')
            print(new_user.usuario_id)
            # Busca pelo id do usuario se tem uma ordem de serviço
            ordem = OrdemDeServico.query.filter_by(usuario_id=new_user.usuario_id).first()
            if ordem is not None:
                data_recebida_dt = datetime.strptime(ordem.data.strftime('%Y-%m-%d'), '%Y-%m-%d')
                data_atual = datetime.now()
                diferenca = data_recebida_dt - data_atual
                if 7 > diferenca.days >= 0:
                    print("A data recebida está dentro dos próximos 7 dias.")
                    return jsonify({'error': 'Post enviado em menos de 7 dias.'}), 403
                else:
                    print("A data recebida está fora dos próximos 7 dias.")
                    #Pega dados do Formumário e enviar nova legenda
                    form = get_formularios_form_id(ordem.id_form)

                    #Monta o data para enviar o dados para legenda nova
                    DadosForm = {
                        "username": form.email_cliente,
                        "email": form.email_cliente,
                        "telefone": form.whatsapp_cliente,
                        "nomenegocio": form.nome_negocio,
                        "socialmedia": form.perfis_redes_sociais_1,
                        "objetivo": form.resumo_cliente,
                        "site": form.site,
                        "nome": form.nome_cliente,
                        "prakem": form.comentarios,
                        "estilo": form.estilo,
                        "cor": form.identidade_visual_1
                    }
                    fluxo = validaFluxo(data)
                    print('enviando criação da legenda para:')

                    envioLegenda = processar_legendas(data, ordem.id_form, fluxo)

                    site = r"http:\\admin.30posts.com.br"

                    # Payload de envio ao cliente inicio de processo
                    payload_img = {
                        "app": KEYTigor,
                        "number": telefone,
                        "message": "Você também pode visualizar os seus posts na plataforma 30 Posts! \n\n " + site + " \n\nSeu Login é: " + email + "\n\nSua Senha: " + password,
                        "type": "text",
                        "url": ""
                    }
                    # Envia mensagem ao cliente
                    requests.post(URLTigor, json=payload_img, headers=headers_Tigor)

                    # VERIFICAR VALIDAÇÃO RETORNO
                    print('**********************************************')
                    print('VOLTOU DO ENVIO')
                    print('**********************************************')

                    return jsonify({'INFO': 'GEROU NOVO POST'}), 200

        # INSERE CLIENTE
        try:
            #Validar se o cliente existe
            existeCliente = Cliente.query.filter_by(email=email).first()
            if existeCliente is None:
                # Insere o cliente na tabela
                cliente = Cliente(
                    nome=username,
                    contato='',
                    segmento='',
                    telefone=telefone,
                    email=email,
                    pais='',
                    tipo_cliente_id=1,
                    ativo=True
                )
                db.session.add(cliente)
                print('Vai inserir cliente')
                db.session.commit()
            else:
                cliente = existeCliente

            # INSERIR NEGOCIO
            try:
                print('BORA INSERIR O NEGOCIO....')
                new_deal = Negocio(cliente_id=cliente.cliente_id, nome_negocio=data.get("nomenegocio"), descricao='',
                                   ativo=True)
                db.session.add(new_deal)
                db.session.commit()
                print('NEGOCIO INSERIDO COM SUCESSO....')
            except Exception as e:
                db.session.rollback()
                error_message = str(e)
                print(error_message)
                return jsonify({'error': 'Erro ao inserir o negócio. Tente novamente.'}), 400

            # INSERIR PEDIDO
            try:
                print('BORA INSERIR O PEDIDO....')
                new_order = Pedido(negocio_id=new_deal.negocio_id, descricao='POST GRATIS VIA WHATS', valor=0.0,
                                   cliente_id=cliente.cliente_id, ativo=True)
                db.session.add(new_order)
                db.session.commit()
                print('PEDIDO INSERIDO COM SUCESSO....')
            except Exception as e:
                db.session.rollback()
                error_message = str(e)
                print(error_message)
                return jsonify({'error': 'Erro ao inserir o pedido. Tente novamente.'}), 400

            # INSERIR ORDEM DE SERVIÇO
            id_form = uuid.uuid4()
            try:
                print('BORA INSERIR O ORDEM DE SERVIÇO....')
                # Adiciona Ordem de serviço
                new_service_order = OrdemDeServico(
                    pedido_id=new_order.pedido_id,
                    descricao='POST GRATIS VIA WHATS',
                    data=datetime.now(),
                    usuario_id=new_user.usuario_id,
                    workflow_id=2,
                    id_negocio=new_deal.negocio_id,
                    id_produto=1,
                    prazointerno=datetime.now(),  # Usando a data corretamente
                    prazoexterno=datetime.now(),  # Usando a data corretamente
                    entrega=datetime.now(),  # Usando a data corretamente
                    mensal=False
                    #id_form=id_form
                )

                db.session.add(new_service_order)
                db.session.commit()
                print('ORDEM DE SERVIÇO INSERIDO COM SUCESSO....')
            except Exception as e:
                db.session.rollback()
                error_message = str(e)
                print(error_message)
                return jsonify({'error': 'Erro ao inserir ordem de serviço. Tente novamente.'}), 400

            # INSERIR FORMULÁRIO
            try:

                print('BORA INSERIR O FORMULÁRIO....')
                # Adiciona o Formulário para preenchimento
                form = FormularioCliente(

                    ordem_id=new_service_order.ordem_id,
                    nome_cliente=username,
                    whatsapp_cliente=telefone,
                    email_cliente=email,
                    id_form=id_form
                )

                db.session.add(form)
                db.session.commit()
                print('FORMULÁRIO: ' + str(id_form) + ' INSERIDO COM SUCESSO....')
            except Exception as e:
                db.session.rollback()
                error_message = str(e)
                print(error_message)
                return jsonify({'error': 'Erro ao inserir FORMULÁRIO. Tente novamente.'}), 400

            #TODO  Atualiza do form na tabela de Ordem de Serviços



            print('enviando criação da legenda para:')
            nomenegocio = data.get("nomenegocio")
            socialmedia = data.get("socialmedia")
            objetivo = data.get("objetivo")

            #print(nomenegocio + ' ' + socialmedia + ' ' + objetivo)
            fluxo = validaFluxo(data)

            envioLegenda = processar_legendas(data, id_form, fluxo)
            #site = r"http:\\plataforma.30posts.com.br"

            # Payload de envio ao cliente inicio de processo
            #payload_img = {
            #    "app": KEYTigor,
            #    "number": telefone,
            #    "message": "Você também pode visualizar os seus posts na plataforma 30 Posts! \n\n " + site + " \n\nSeu Login é: " + email + "\n\nSua Senha: " + password,
            #    "type": "text",
            #    "url": ""
            #}
            # Envia mensagem ao cliente
            #requests.post(URLTigor, json=payload_img, headers=headers_Tigor)

            # VERIFICAR VALIDAÇÃO RETORNO
            print('**********************************************')
            print('VOLTOU DO ENVIO')
            print('**********************************************')
            return jsonify(cliente.serialize()), 201

        except Exception as e:
            db.session.rollback()
            error_message = str(e)
            print(error_message)
            return jsonify({'error': 'Erro ao inserir o cliente. Tente novamente.'}), 400

    except IntegrityError as e:
        print('Erro de Integridade!')
        db.session.rollback()
        error_message = str(e)
        # Verifica se 'UniqueViolation' está na mensagem de erro
        if "UniqueViolation" in error_message:
            # Mensagem amigável para o usuário
            return jsonify(
                {'error': 'Erro: Este nome de usuário ou e-mail já está em uso. Por favor, escolha outro.'}), 400
        else:
            return jsonify({'error': 'Ocorreu um erro ao tentar criar o usuário. Tente novamente mais tarde.'}), 400
