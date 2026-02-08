from flask_cors import CORS
from dotenv import load_dotenv
from flasgger import Swagger
load_dotenv()

from flask import Flask

from src.app.externals.db.connection import engine
from src.app.externals.models import Category, Transaction, User
from src.app.externals.models.base import Base

from src.app.controllers.user_controller import user_bp
from src.app.controllers.category_controller import category_bp
from src.app.controllers.transaction_controller import transaction_bp
from src.app.controllers.auth_controller import auth_bp
from src.app.controllers.transaction_controller import transaction_bp


import logging

def create_app():
    # Configuração de Logs
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    app = Flask(__name__)
    CORS(app)
    
    # Configuração do Swagger
    app.config['SWAGGER'] = {
        'title': 'FinancePlus API',
        'uiversion': 3,
        'description': 'API para gerenciamento financeiro pessoal',
        'version': '1.0.0',
        'specs_route': '/apidocs/'
    }
    Swagger(app)

    # Criar todas as tabelas (uma única vez)
    with app.app_context():
        Base.metadata.create_all(bind=engine)

    @app.route("/")
    def home():
        return "FinancePlus API - funcionando! 🚀"

    @app.route("/health")
    def health():
        return {"status": "ok"}, 200
    
    app.register_blueprint(user_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(auth_bp)

    return app


