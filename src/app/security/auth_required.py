from functools import wraps
from flask import request, jsonify
from src.app.security.jwt_utils import verify_token


def auth_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Token não enviado"}), 401

        parts = auth_header.split(" ")

        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({"error": "Formato inválido de token"}), 401

        token = parts[1]
        user_id = verify_token(token)

        if not user_id:
            return jsonify({"error": "Token inválido ou expirado"}), 401

        # 🔥 AQUI ESTÁ A CORREÇÃO
        request.user_id = user_id

        return f(*args, **kwargs)

    return wrapper
