from flask import Flask
from models import init_app
from models.clientes import clientes_bp
from models.negocios import negocios_bp
from models.ordens_de_servico import ordens_de_servico_bp
from models.informacoes_clientes import informacoes_clientes_bp
from models.pedidos import pedidos_bp

app = Flask(__name__)
app.config.from_object('config.Config')

init_app(app)

app.register_blueprint(clientes_bp, url_prefix='/clientes')
app.register_blueprint(negocios_bp, url_prefix='/negocios')
app.register_blueprint(ordens_de_servico_bp, url_prefix='/ordens_de_servico')
app.register_blueprint(informacoes_clientes_bp, url_prefix='/informacoes_clientes')
app.register_blueprint(pedidos_bp, url_prefix='/pedidos')

if __name__ == '__main__':
    app.run(debug=True)
