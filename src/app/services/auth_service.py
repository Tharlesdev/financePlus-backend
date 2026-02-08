from src.app.repositories.user_repository import UserRepository
from src.app.externals.exceptions import PasswordIncorrectException


class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()

    def register(self, data: dict):
        try:
            name = data.get("name")
            email = data.get("email")
            password = data.get("password")

            if not name or not email or not password:
                return {"error": "Campos obrigatórios faltando"}, 400

            existing = self.user_repo.get_by_email(email)
            if existing:
                return {"error": "E-mail já registrado"}, 409

            user_data = {
                "name": name,
                "email": email,
                "password": password
            }
            # UserRepository.create_user retorna dict
            user_dict = self.user_repo.create_user(user_data)

            return user_dict, 201

        except Exception as e:
             return {"error": str(e)}, 500

    def login(self, email: str, password: str):
        try:
            user = self.user_repo.get_by_email(email)
            if not user:
                return None

            user.validate_password(password)
            return user
        
        except PasswordIncorrectException:
            return None
        except Exception:
            return None
    
    def get_me(self, user_id: str):
        # user_repo.get_user_by_id retorna dict. 
        # Se quisermos retornar dict, tudo bem.
        return self.user_repo.get_user_by_id(user_id)




auth_service = AuthService()
