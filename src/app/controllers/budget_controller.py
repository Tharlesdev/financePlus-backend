from flask import Blueprint, request, jsonify
from src.app.services.budget_service import BudgetService
from src.app.schemas.budget_schemas import BudgetCreate
from src.app.security.auth_required import auth_required
from pydantic import ValidationError
from datetime import datetime

budget_bp = Blueprint("budget_bp", __name__, url_prefix="/budgets")
service = BudgetService()

@budget_bp.route("/", methods=["POST"])
@auth_required
def create_budget():
    """
    Cria ou atualiza uma meta de orçamento (Budget)
    ---
    tags:
      - Budgets
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            category_id:
              type: string
            amount:
              type: number
            month:
              type: string
              example: "2023-10"
    responses:
      201:
        description: Budget criado
      400:
        description: Erro de validação
    """
    try:
        data = request.get_json()
        data["user_id"] = request.user_id
        
        # Validar schema
        schema = BudgetCreate(**data)
        
        budget = service.create_budget(data)
        
        return jsonify({
            "id": budget.id,
            "category_id": budget.category_id,
            "amount": budget.amount,
            "month": budget.month
        }), 201

    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

@budget_bp.route("/", methods=["GET"])
@auth_required
def get_budgets():
    """
    Lista budgets e status de consumo para um mês
    ---
    tags:
      - Budgets
    parameters:
      - in: query
        name: month
        type: string
        required: true
        description: Mês no formato YYYY-MM
    """
    month = request.args.get("month")
    if not month:
        # Default para mês atual
        month = datetime.now().strftime("%Y-%m")
        
    status = service.get_budgets_status(request.user_id, month)
    return jsonify(status), 200

@budget_bp.route("/<budget_id>", methods=["DELETE"])
@auth_required
def delete_budget(budget_id):
    success = service.delete_budget(budget_id)
    if success:
        return jsonify({"message": "Budget removido"}), 200
    return jsonify({"error": "Budget não encontrado"}), 404
