from flask import Blueprint, request, jsonify
from src.app.services.user_service import UserService
from src.app.schemas.user_schemas import UserCreate, UserUpdate
from pydantic import ValidationError

user_bp = Blueprint("user", __name__, url_prefix="/users")
service = UserService()


@user_bp.route("/", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        validated_data = UserCreate(**data)
        
        user = service.create_user(validated_data.model_dump())
        return jsonify(user), 201
    except ValidationError as e:
        return jsonify(e.errors()), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@user_bp.route("/", methods=["GET"])
def list_users():
    users = service.get_all_users()
    return jsonify(users), 200


@user_bp.route("/<uuid:user_id>", methods=["GET"])
def get_user(user_id):
    user = service.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404
    return jsonify(user), 200


@user_bp.route("/<uuid:user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        data = request.get_json()
        validated_data = UserUpdate(**data)
        # exclude_unset=True para ignorar campos não enviados
        service_data = validated_data.model_dump(exclude_unset=True)
        
        user = service.update_user(user_id, service_data)
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        return jsonify(user), 200
        
    except ValidationError as e:
        return jsonify(e.errors()), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@user_bp.route("/<uuid:user_id>", methods=["DELETE"])
def delete_user(user_id):
    deleted = service.delete_user(user_id)
    if not deleted:
        return jsonify({"error": "Usuário não encontrado"}), 404
    return jsonify({"message": "Usuário removido com sucesso"}), 200