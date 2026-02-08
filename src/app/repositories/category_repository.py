from src.app.externals.db.connection import SessionLocal
from src.app.externals.models.category import Category
import uuid

class CategoryRepository:
    def create_category(self, data):
        session = SessionLocal()
        try:
            if "user_id" in data and isinstance(data["user_id"], str):
                data["user_id"] = uuid.UUID(data["user_id"])
            category = Category(**data)
            session.add(category)
            session.commit()
            session.refresh(category)
            return category.as_dict
        finally:
            session.close()

    def get_all_categories(self):
        session = SessionLocal()
        try:
            categories = session.query(Category).all()
            return [c.as_dict for c in categories]
        finally:
            session.close()

    def get_category_by_id(self, category_id):
        session = SessionLocal()
        try:
            category = session.get(Category, category_id)
            return category.as_dict if category else None
        finally:
            session.close()

    def update_category(self, category_id, data):
        session = SessionLocal()
        try:
            category = session.get(Category, category_id)
            if not category:
                return None

            for key, value in data.items():
                setattr(category, key, value)

            session.commit()
            session.refresh(category)
            return category.as_dict
        finally:
            session.close()

    def delete_category(self, category_id):
        session = SessionLocal()
        try:
            category = session.get(Category, category_id)
            if not category:
                return False

            session.delete(category)
            session.commit()
            return True
        finally:
            session.close()
