from flask import Blueprint, request, jsonify
from . import db
from utils.token_verify import token_required  

form_bp = Blueprint('form', __name__)

@form_bp.route('/', methods=['GET'])
@token_required
def send_form(token_data):
    form_id = token_data.get('id')

    return jsonify({'id': form_id})