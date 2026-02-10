from flask import Blueprint, request, jsonify, send_file
from uuid import UUID

from src.app.services.transaction_service import transaction_service
from src.app.services.export_service import ExportService
from src.app.security.auth_required import auth_required
from src.app.schemas.transaction_schemas import TransactionCreate
from pydantic import ValidationError

transaction_bp = Blueprint("transaction", __name__, url_prefix="/transactions")
export_service = ExportService()


# -------------------------------------------
# EXPORT (CSV/Excel)
# -------------------------------------------
@transaction_bp.route("/export/csv", methods=["GET"])
@auth_required
def export_csv():
    filters = dict(request.args)
    filters["user_id"] = request.user_id
    
    output = export_service.export_transactions_csv(filters)
    if not output:
        return jsonify({"error": "Nenhum dado para exportar"}), 404
        
    return send_file(
        output,
        mimetype="text/csv",
        as_attachment=True,
        download_name="transactions.csv"
    )

@transaction_bp.route("/export/excel", methods=["GET"])
@auth_required
def export_excel():
    filters = dict(request.args)
    filters["user_id"] = request.user_id
    
    output = export_service.export_transactions_excel(filters)
    if not output:
        return jsonify({"error": "Nenhum dado para exportar"}), 404
        
    return send_file(
        output,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name="transactions.xlsx"
    )


# -------------------------------------------
# LIST (com filtros)
# -------------------------------------------
@transaction_bp.route("/", methods=["GET"])
@auth_required
def list_transactions():
    filters = dict(request.args)

    # 🔥 user_id vem SEMPRE do token
    filters["user_id"] = request.user_id

    result = transaction_service.list(filters)

    # caso de erro
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]

    return jsonify(result), 200


# -------------------------------------------
# CREATE
# -------------------------------------------
@transaction_bp.route("/", methods=["POST"])
@auth_required
def create_transaction():
    data = request.json
    validated_data = TransactionCreate(**data)
    
    service_data = validated_data.model_dump()
    # user_id sempre vem do token
    service_data["user_id"] = request.user_id

    created = transaction_service.create_transaction(service_data)
    return jsonify(created), 201


# -------------------------------------------
# GET BY ID (somente se for dono)
# -------------------------------------------
@transaction_bp.route("/<transaction_id>", methods=["GET"])
@auth_required
def get_transaction(transaction_id):
    transaction = transaction_service.get_transaction_by_id(transaction_id)

    if not transaction:
        return jsonify({"error": "Transação não encontrada"}), 404

    if transaction["user_id"] != str(request.user_id):
        return jsonify({"error": "Acesso negado"}), 403

    return jsonify(transaction), 200


# -------------------------------------------
# UPDATE (somente se for dono)
# -------------------------------------------
@transaction_bp.route("/<transaction_id>", methods=["PUT"])
@auth_required
def update_transaction(transaction_id):
    data = request.json
    # Para update, talvez nem todos os campos sejam obrigatórios. 
    # Mas vamos usar TransactionCreate por enquanto ou criar TransactionUpdate.
    # Se TransactionCreate exige tudo, o update vai exigir tudo.
    # Vamos assumir que PUT substitui o recurso (padrão REST), então exigir tudo é ok.
    validated_data = TransactionCreate(**data)
    
    # valida dono
    existing = transaction_service.get_transaction_by_id(transaction_id)
    if not existing:
        return jsonify({"error": "Transação não encontrada"}), 404

    if existing["user_id"] != str(request.user_id):
        return jsonify({"error": "Acesso negado"}), 403

    updated = transaction_service.update_transaction(transaction_id, validated_data.model_dump())
    return jsonify(updated), 200


# -------------------------------------------
# DELETE (somente se for dono)
# -------------------------------------------
@transaction_bp.route("/<transaction_id>", methods=["DELETE"])
@auth_required
def delete_transaction(transaction_id):

    # valida dono
    existing = transaction_service.get_transaction_by_id(transaction_id)
    if not existing:
        return jsonify({"error": "Transação não encontrada"}), 404

    if existing["user_id"] != str(request.user_id):
        return jsonify({"error": "Acesso negado"}), 403

    deleted = transaction_service.delete_transaction(transaction_id)
    if not deleted:
        return jsonify({"error": "Erro ao apagar transação"}), 400

    return jsonify({"message": "Transação removida com sucesso"}), 200
