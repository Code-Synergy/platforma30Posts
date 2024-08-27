from flask import Blueprint, jsonify, current_app
import jwt
import datetime

from models.formulario_cliente import FormularioCliente

valida_id_form_bp = Blueprint('valida', __name__)

@valida_id_form_bp.route('/<string:id>', methods=['GET'])
def valida_id_form(id):
    print(id)
    form = FormularioCliente.query.filter_by(id_form=id);
    if(form):
        token = jwt.encode({
                'id': id,
                'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)
            }, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'Not Found!'}), 404