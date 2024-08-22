from flask import Blueprint, request, jsonify
from . import db

legendas_bp = Blueprint('legendas', __name__)

class Legenda(db.Model):
    __tablename__ = 'legendas'

    id_legenda = db.Column(db.Integer, primary_key=True)
    id_form = db.Column(db.Integer, db.ForeignKey('formulario_cliente.form_id'), primary_key=True)
    dia_post = db.Column(db.String(10), primary_key=True)
    ds_legenda = db.Column(db.Text, nullable=False)

    def __init__(self, id_form, dia_post, ds_legenda):
        self.id_form = id_form
        self.dia_post = dia_post
        self.ds_legenda = ds_legenda

@legendas_bp.route('/', methods=['GET'])
def get_legendas():
    legendas = Legenda.query.all()
    return jsonify([l.serialize() for l in legendas])

@legendas_bp.route('/', methods=['POST'])
def add_legenda():
    data = request.get_json()
    legenda = Legenda(
        id_form=data['id_form'],
        dia_post=data['dia_post'],
        ds_legenda=data['ds_legenda']
    )
    db.session.add(legenda)
    db.session.commit()
    return jsonify(legenda.serialize()), 201

@legendas_bp.route('/<int:id_legenda>/<int:id_form>/<string:dia_post>', methods=['PUT'])
def update_legenda(id_legenda, id_form, dia_post):
    legenda = Legenda.query.get_or_404((id_legenda, id_form, dia_post))
    data = request.get_json()

    legenda.ds_legenda = data.get('ds_legenda', legenda.ds_legenda)

    db.session.commit()
    return jsonify(legenda.serialize())

@legendas_bp.route('/<int:id_legenda>/<int:id_form>/<string:dia_post>', methods=['DELETE'])
def delete_legenda(id_legenda, id_form, dia_post):
    legenda = Legenda.query.get_or_404((id_legenda, id_form, dia_post))
    db.session.delete(legenda)
    db.session.commit()
    return '', 204
