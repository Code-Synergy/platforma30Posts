from flask_sqlalchemy import SQLAlchemy

# Inicializar a instância do SQLAlchemy
db = SQLAlchemy()

def init_app(app):
    # Configurar o SQLAlchemy com o aplicativo Flask
    db.init_app(app)

    # Se desejar criar todas as tabelas automaticamente (útil para desenvolvimento)
    with app.app_context():
        db.create_all()
