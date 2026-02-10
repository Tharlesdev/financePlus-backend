from flask import Blueprint, jsonify, request
from src.app.services.dashboard_service import dashboard_service
from src.app.security.auth_required import auth_required

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@dashboard_bp.route("", methods=["GET"])
@auth_required
def get_dashboard():
    """
    Retorna dados para o dashboard:
    - Balanço mensal (receita, despesa, saldo)
    - Despesas por categoria
    - Insights (taxa de poupança, maior despesa, totais)
    """
    user_id = request.user_id
    data = dashboard_service.get_dashboard_data(user_id)
    return jsonify(data), 200
