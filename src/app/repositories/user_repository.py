from src.app.externals.db.connection import SessionLocal
from src.app.externals.models.user import User
import uuid

class UserRepository:
    def create_user(self, data):
        session = SessionLocal()
        user = User(
            name=data["name"],
            email=data["email"],
            password=data["password"]
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        session.close()
        return user.as_dict

    def get_all_users(self):
        session = SessionLocal()
        users = session.query(User).all()
        session.close()
        return [u.as_dict for u in users]

    def get_user_by_id(self, user_id):
        session = SessionLocal()
        if isinstance(user_id, str):
            user_id = uuid.UUID(user_id)
        user = session.get(User, user_id)
        session.close()
        return user.as_dict if user else None

    def get_by_email(self, email):
        session = SessionLocal()
        try:
            user = session.query(User).filter(User.email == email).first()
            return user
        finally:
            session.close()

    def update_user(self, user_id, data):
        session = SessionLocal()
        user = session.get(User, user_id)
        if not user:
            session.close()
            return None

        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        session.commit()
        session.refresh(user)
        session.close()
        return user.as_dict

    def delete_user(self, user_id):
        session = SessionLocal()
        user = session.get(User, user_id)
        if not user:
            session.close()
            return False
        session.delete(user)
        session.commit()
        session.close()
        return True
