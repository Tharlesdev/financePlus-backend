from flask import jsonify
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException

def register_error_handlers(app):
    
    @app.errorhandler(ValidationError)
    def handle_pydantic_error(e):
        return jsonify({"error": "Dados inválidos", "details": e.errors()}), 400

    @app.errorhandler(404)
    def handle_not_found(e):
        return jsonify({"error": "Recurso não encontrado"}), 404
    
    @app.errorhandler(401)
    def handle_unauthorized(e):
        return jsonify({"error": "Não autorizado"}), 401
        
    @app.errorhandler(403)
    def handle_forbidden(e):
        return jsonify({"error": "Acesso negado"}), 403

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return jsonify({"error": e.description}), e.code

    # Captura genérica para exceções não tratadas (opcional, mas cuidado para não expor detalhes sensíveis em prod)
    @app.errorhandler(Exception)
    def handle_generic_exception(e):
        # Em produção, logar o erro real aqui
        print(f"Erro não tratado: {e}")
        return jsonify({"error": "Ocorreu um erro inesperado"}), 500
