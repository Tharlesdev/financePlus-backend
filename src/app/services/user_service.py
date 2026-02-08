from src.app.repositories.user_repository import UserRepository

class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def create_user(self, data):
        return self.repo.create_user(data)

    def get_all_users(self):
        return self.repo.get_all_users()

    def get_user_by_id(self, user_id):
        return self.repo.get_user_by_id(user_id)

    def update_user(self, user_id, data):
        return self.repo.update_user(user_id, data)

    def delete_user(self, user_id):
        return self.repo.delete_user(user_id)