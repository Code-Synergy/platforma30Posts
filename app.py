from flask import Flask
from flask_jwt_extended import JWTManager
from models import db, clientes, pedido, ordens_de_servico, negocios, send_form, validar_id_form, workflow, legendas, tipo_cliente, user
from config import Config
from flask_cors import CORS

from models import formulario_cliente

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Certifique-se de que SQLALCHEMY_DATABASE_URI esteja definida
app.config['SQLALCHEMY_DATABASE_URI'] = Config.DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
jwt = JWTManager(app)

# Registrar blueprints
app.register_blueprint(clientes.clientes_bp, url_prefix='/clientes')
app.register_blueprint(ordens_de_servico.ordens_de_servico_bp, url_prefix='/ordens_de_servico')
app.register_blueprint(negocios.negocios_bp, url_prefix='/negocios')
app.register_blueprint(workflow.workflow_bp, url_prefix='/workflow')
app.register_blueprint(formulario_cliente.formulario_cliente_bp, url_prefix='/formulario_cliente')
app.register_blueprint(legendas.legendas_bp, url_prefix='/legendas')
app.register_blueprint(tipo_cliente.tipo_de_cliente_bp, url_prefix='/tipo_cliente')
app.register_blueprint(user.user_bp, url_prefix='/user')
app.register_blueprint(validar_id_form.valida_id_form_bp, url_prefix='/valida')
app.register_blueprint(send_form.form_bp, url_prefix='/form')
app.register_blueprint(pedido.pedidos_bp, url_prefix='/pedidos')


if __name__ == '__main__':
    app.run(debug=True)
