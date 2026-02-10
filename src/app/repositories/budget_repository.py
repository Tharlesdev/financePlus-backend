from src.app.externals.db.connection import SessionLocal
from src.app.externals.models.budget import Budget
from uuid import UUID

class BudgetRepository:
    def create(self, data: dict):
        session = SessionLocal()
        try:
            # Converter UUIDs se string
            if isinstance(data.get("user_id"), str):
                data["user_id"] = UUID(data["user_id"])
            
            # category_id pode vir como UUID do Pydantic ou str
            if isinstance(data.get("category_id"), str):
                data["category_id"] = UUID(data["category_id"])

            # Verifica se já existe budget para essa categoria no mês
            existing = session.query(Budget).filter_by(
                user_id=data["user_id"],
                category_id=data["category_id"],
                month=data["month"]
            ).first()

            if existing:
                existing.amount = data["amount"]
                session.commit()
                session.refresh(existing)
                return existing

            new_budget = Budget(**data)
            session.add(new_budget)
            session.commit()
            session.refresh(new_budget)
            return new_budget
        finally:
            session.close()

    def get_by_user_and_month(self, user_id, month: str):
        session = SessionLocal()
        try:
            if isinstance(user_id, str):
                user_id = UUID(user_id)
            return session.query(Budget).filter_by(user_id=user_id, month=month).all()
        finally:
            session.close()
    
    def get_by_id(self, budget_id):
        session = SessionLocal()
        try:
            if isinstance(budget_id, str):
                budget_id = UUID(budget_id)
            return session.query(Budget).filter_by(id=budget_id).first()
        finally:
            session.close()

    def delete(self, budget_id):
        session = SessionLocal()
        try:
            if isinstance(budget_id, str):
                budget_id = UUID(budget_id)
            budget = session.query(Budget).filter_by(id=budget_id).first()
            if budget:
                session.delete(budget)
                session.commit()
                return True
            return False
        finally:
            session.close()
