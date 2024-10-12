from flask import request, jsonify
from . import db, user
from datetime import date
import requests

#API de envio de mensagem Whats
URLTigor = "https://tigor.itlabs.app/wpp/api"
KEYTigor = "3bd82d2e-3077-4226-a366-1338eb3ed589"
headers_Tigor = {"Content-Type": "application/json"}

class BalanceSM(db.Model):
    __tablename__ = 'balancesm'

    id = db.Column(db.Integer, primary_key=True)
    id_form = db.Column(db.String(255), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.usuario_id'))
    status_os = db.Column(db.Integer)
    datainc = db.Column(db.Date)

    def __init__(self, id_form, usuario_id, status_os, datainc):
        self.id_form = id_form
        self.usuario_id = usuario_id
        self.status_os = status_os
        self.datainc = datainc

    def serialize(self):
        return {
            'id': self.id,
            'id_form': self.id_form,
            'usuario_id': self.usuario_id,
            'status_os': self.status_os,
            'datainc': self.datainc.isoformat() if self.datainc else None
        }

def distribuir_ordem(id_form):
    #data = request.get_json()
    #id_form = data['id_form']

    # Buscar todos os Social Medias
    print('*************************************************')
    print('************************************************')
    print('************************************************')
    print('     ESTAMOS NA DISTRIBUIÇÃO     ')
    print('************************************************')
    print('************************************************')
    print('************************************************')

    print(id_form)
    social_medias = user.Usuarios.query.filter_by(perfil_id=4).all()
    print(social_medias)

    # Se não houver Social Medias, retornar erro
    if not social_medias:
        return jsonify({"message": "Nenhum Social Media encontrado"}), 404

    # Contar quantas OS ativas cada Social Media tem na tabela balancesm
    print(' Contar quantas OS ativas cada Social Media tem na tabela balancesm')
    social_medias_com_os = []
    for sm in social_medias:
        print(sm.usuario_id)
        count = BalanceSM.query.filter_by(usuario_id=sm.usuario_id, status_os=1).count()  # status 1 = ativo
        print(count)
        social_medias_com_os.append({'usuario': sm, 'ordens_ativas': count})

    # Verificar se o Social Media já tem 4 ou mais OSs ativas e apenas imprimir um aviso
    if count >= 4:
        print('*************************************************')
        print('************************************************')
        print('************************************************')
        print('     maior de 4 dispara mensagem     ')
        print('************************************************')
        print('************************************************')
        print('************************************************')
        URLTigor = "https://tigor.itlabs.app/wpp/api"
        whatsCliente = '11998637834'
        payload = {
            "app": "3bd82d2e-3077-4226-a366-1338eb3ed589",
            "number": whatsCliente,
            "message": "ALERTA: SOCIAL MEDIA COM GARGALO",
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
            print('ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR :')
            print(responseWhats.text)
            print(responseWhats.status_code)
            return jsonify({responseWhats}), 500

        print('MENSAGEM ENVIADA')
        
    social_medias_com_os.append({'usuario': sm, 'ordens_ativas': count})

    # Ordenar pelo número de OSs ativas (ordem crescente)
    social_medias_com_os.sort(key=lambda x: x['ordens_ativas'])

    # Pegar o primeiro Social Media com menos OSs ativas
    escolhido = social_medias_com_os[0]['usuario']

    # Criar nova Ordem de Serviço e associar ao Social Media escolhido
    nova_ordem = BalanceSM(
        id_form=id_form,
        usuario_id=escolhido.usuario_id,
        status_os=1,  # status ativo
        datainc=date.today()
    )

    db.session.add(nova_ordem)
    db.session.commit()

    return jsonify(nova_ordem.serialize()), 201
