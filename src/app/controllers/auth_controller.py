from flask import Blueprint, request, jsonify
from src.app.services.auth_service import auth_service
from src.app.security.auth_required import auth_required
from src.app.security.jwt_utils import create_token
from src.app.schemas.user_schemas import UserCreate, UserLogin
from pydantic import ValidationError

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.json
        user_data = UserCreate(**data)
        
        # Converter para dict para passar para o service
        # (O service espera dict por enquanto, idealmente refatoraríamos para aceitar schema)
        result, status = auth_service.register(user_data.model_dump())
        return jsonify(result), status
        
    except ValidationError as e:
        return jsonify(e.errors()), 400


@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        login_data = UserLogin(**data)

        user = auth_service.login(login_data.email, login_data.password)

        if not user:
            return jsonify({"error": "Credenciais inválidas"}), 401

        # gera token JWT
        token = create_token(user_id=str(user.id))

        return jsonify({
            "access_token": token,
            "token_type": "Bearer"
        }), 200
        
    except ValidationError as e:
        return jsonify(e.errors()), 400

@auth_bp.route("/me", methods=["GET"])
@auth_required
def me():
    user = auth_service.get_me(request.user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "user_id": user["id"],
        "name": user["name"],
        "email": user["email"]
    }), 200
