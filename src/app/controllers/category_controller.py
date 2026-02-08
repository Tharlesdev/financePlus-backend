from flask import Blueprint, jsonify, request
from src.app.services.category_service import CategoryService
from src.app.security.auth_required import auth_required
from src.app.schemas.category_schemas import CategoryCreate
from pydantic import ValidationError

category_bp = Blueprint("category", __name__, url_prefix="/categories")
service = CategoryService()


@category_bp.route("/", methods=["POST"])
@auth_required
def create_category():
    try:
        data = request.json
        validated_data = CategoryCreate(**data)
        
        service_data = validated_data.model_dump()
        service_data["user_id"] = request.user_id

        category = service.create_category(service_data)

        return jsonify(category), 201
        
    except ValidationError as e:
        return jsonify(e.errors()), 400


@category_bp.route("/", methods=["GET"])
@auth_required
def list_categories():
    categories = service.get_all_categories()
    return jsonify(categories), 200


@category_bp.route("/<uuid:category_id>", methods=["GET"])
@auth_required
def get_category(category_id):
    category = service.get_category_by_id(category_id)
    if not category:
        return jsonify({"error": "Category not found"}), 404
    return jsonify(category), 200


@category_bp.route("/<uuid:category_id>", methods=["PUT"])
@auth_required
def update_category(category_id):
    try:
        data = request.get_json()
        validated_data = CategoryCreate(**data) # Using same schema for update for now
        
        category = service.update_category(category_id, validated_data.model_dump())
        if not category:
            return jsonify({"error": "Category not found"}), 404
        return jsonify(category), 200
        
    except ValidationError as e:
        return jsonify(e.errors()), 400


@category_bp.route("/<uuid:category_id>", methods=["DELETE"])
@auth_required
def delete_category(category_id):
    success = service.delete_category(category_id)
    if not success:
        return jsonify({"error": "Category not found"}), 404
    return jsonify({"message": "Category deleted"}), 200
