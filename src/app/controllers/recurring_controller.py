from flask import Blueprint, request, jsonify
from src.app.services.recurring_service import RecurringService
from src.app.schemas.recurring_schemas import RecurringTransactionCreate
from src.app.security.auth_required import auth_required
from pydantic import ValidationError

recurring_bp = Blueprint("recurring_bp", __name__, url_prefix="/recurring")
service = RecurringService()

@recurring_bp.route("/", methods=["POST"])
@auth_required
def create_recurring():
    """
    Cria uma transação recorrente
    ---
    tags:
      - Recurring
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            category_id:
              type: string
            description:
              type: string
            amount:
              type: number
            type:
              type: string
              enum: [income, expense]
            frequency:
              type: string
              enum: [weekly, monthly, yearly]
            start_date:
              type: string
              format: date
    """
    try:
        data = request.get_json()
        data["user_id"] = request.user_id
        
        # Validar schema
        schema = RecurringTransactionCreate(**data)
        
        # Converte date string para objeto date se necessário (pydantic faz isso, mas para o dict precisamos tratar)
        # O Pydantic já validou, mas o dict raw ainda tem string. 
        # Vamos passar os dados validados do schema.
        clean_data = schema.model_dump()
        clean_data["user_id"] = request.user_id
        
        rec = service.create_recurring(clean_data)
        
        return jsonify({
            "id": rec.id,
            "description": rec.description,
            "next_run": rec.next_run.isoformat()
        }), 201
        
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

@recurring_bp.route("/", methods=["GET"])
@auth_required
def list_recurring():
    """
    Lista transações recorrentes do usuário
    """
    items = service.get_user_recurring(request.user_id)
    result = []
    for item in items:
        result.append({
            "id": item.id,
            "description": item.description,
            "amount": item.amount,
            "frequency": item.frequency,
            "next_run": item.next_run.isoformat(),
            "active": item.active
        })
    return jsonify(result), 200

@recurring_bp.route("/process", methods=["POST"])
# @auth_required 
# Deixando aberto para cron jobs locais por enquanto
def process_recurring():
    """
    Gatilho manual para processar recorrentes vencidas
    """
    count = service.process_due_transactions()
    return jsonify({"processed": count, "message": "Processamento concluído"}), 200
