from src.app.externals.db.connection import SessionLocal
from src.app.externals.models.recurring_transaction import RecurringTransaction
from datetime import date
from uuid import UUID

class RecurringRepository:
    def create(self, data: dict):
        session = SessionLocal()
        try:
            # Converter UUIDs se string
            if isinstance(data.get("user_id"), str):
                data["user_id"] = UUID(data["user_id"])
            
            if isinstance(data.get("category_id"), str):
                data["category_id"] = UUID(data["category_id"])

            # next_run começa como start_date
            data["next_run"] = data["start_date"]
            new_tx = RecurringTransaction(**data)
            session.add(new_tx)
            session.commit()
            session.refresh(new_tx)
            return new_tx
        finally:
            session.close()

    def get_all_by_user(self, user_id):
        session = SessionLocal()
        try:
            if isinstance(user_id, str):
                user_id = UUID(user_id)
            return session.query(RecurringTransaction).filter_by(user_id=user_id).all()
        finally:
            session.close()

    def get_due_transactions(self):
        """Retorna transações ativas que precisam ser executadas (next_run <= hoje)"""
        session = SessionLocal()
        try:
            today = date.today()
            return session.query(RecurringTransaction).filter(
                RecurringTransaction.active == True,
                RecurringTransaction.next_run <= today
            ).all()
        finally:
            session.close()

    def update(self, transaction_id, updates: dict):
        session = SessionLocal()
        try:
            if isinstance(transaction_id, str):
                transaction_id = UUID(transaction_id)
            tx = session.query(RecurringTransaction).filter_by(id=transaction_id).first()
            if tx:
                for key, value in updates.items():
                    setattr(tx, key, value)
                session.commit()
                session.refresh(tx)
                return tx
            return None
        finally:
            session.close()
