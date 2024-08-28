from flask import Blueprint, jsonify, current_app
import jwt
import datetime

from models.formulario_cliente import FormularioCliente
from models.ordens_de_servico import OrdemDeServico
from models.workflow import Workflow

valida_id_form_bp = Blueprint('valida', __name__)

@valida_id_form_bp.route('/<string:id>', methods=['GET'])
def valida_id_form(id):
    form = FormularioCliente.query.get(id)
    if form and form.ordem_id:
        ordem = OrdemDeServico.query.get(form.ordem_id)
        if ordem and ordem.workflow_id:
            workflow = Workflow.query.get(ordem.workflow_id)
            if workflow:
                token = jwt.encode({
                    'id': id,
                    'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
                }, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
                return jsonify({
                    'token': token,
                    'status': workflow.workflow_id
                }), 200
    return jsonify({'message': 'Not Found!'}), 404
