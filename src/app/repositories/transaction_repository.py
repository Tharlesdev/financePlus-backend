from src.app.externals.db.connection import SessionLocal
from src.app.externals.models.transaction import Transaction
from uuid import UUID
from datetime import datetime

class TransactionRepository:
    def create_transaction(self, data):
        db = SessionLocal()
        try:
            # Converter UUIDs se necessário
            if isinstance(data.get("user_id"), str):
                data["user_id"] = UUID(data["user_id"])
            
            if data.get("category_id") and isinstance(data["category_id"], str):
                data["category_id"] = UUID(data["category_id"])
            elif "category_id" in data and not data["category_id"]:
                 data["category_id"] = None

            # amount deve ser float/decimal
            if "amount" in data:
                data["amount"] = float(data["amount"])

            transaction = Transaction(**data)
            db.add(transaction)
            db.commit()
            db.refresh(transaction)
            return transaction.as_dict
        finally:
            db.close()

    def get_all_transactions(self):
        db = SessionLocal()
        try:
            transactions = db.query(Transaction).all()
            return [t.as_dict for t in transactions]
        finally:
            db.close()

    def get_transaction_by_id(self, transaction_id):
        db = SessionLocal()
        try:
            transaction = db.get(Transaction, transaction_id)
            return transaction.as_dict if transaction else None
        finally:
            db.close()

    def update_transaction(self, transaction_id, data):
        db = SessionLocal()
        try:
            transaction = db.get(Transaction, transaction_id)
            if not transaction:
                return None

            for key, value in data.items():
                if key in ["user_id", "category_id"] and value and isinstance(value, str):
                    value = UUID(value)
                setattr(transaction, key, value)

            db.commit()
            db.refresh(transaction)
            return transaction.as_dict
        finally:
            db.close()

    def delete_transaction(self, transaction_id):
        db = SessionLocal()
        try:
            transaction = db.get(Transaction, transaction_id)
            if not transaction:
                return False

            db.delete(transaction)
            db.commit()
            return True
        finally:
            db.close()

    def list(self, filters: dict):
        db = SessionLocal()
        try:
            query = db.query(Transaction)

            # 🟦 user_id (OBRIGATÓRIO)
            user_id = filters.get("user_id")
            if not user_id:
                # Retornar lista vazia ou erro? Repository geralmente não retorna erro HTTP.
                # Vamos assumir que quem chama garante ou filtramos vazio se não tiver user_id.
                # O código original retornava erro 400. Vamos manter comportamento seguro.
                return [] 
            
            if isinstance(user_id, str):
                 user_id = UUID(user_id)
            query = query.filter(Transaction.user_id == user_id)

            # 🟦 category_id
            category_id = filters.get("category_id")
            if category_id:
                if isinstance(category_id, str):
                    category_id = UUID(category_id)
                query = query.filter(Transaction.category_id == category_id)

            # 🟦 tipo
            type_ = filters.get("type")
            if type_:
                query = query.filter(Transaction.type == type_)

            # 🟦 start_date
            start_date = filters.get("start_date")
            if start_date:
                try:
                    start_date = datetime.fromisoformat(start_date)
                    query = query.filter(Transaction.created_at >= start_date)
                except ValueError:
                    pass

            # 🟦 end_date
            end_date = filters.get("end_date")
            if end_date:
                try:
                    end_date = datetime.fromisoformat(end_date)
                    query = query.filter(Transaction.created_at <= end_date)
                except ValueError:
                    pass

            # 🟦 min_amount
            min_amount = filters.get("min_amount")
            if min_amount:
                query = query.filter(Transaction.amount >= float(min_amount))

            # 🟦 max_amount
            max_amount = filters.get("max_amount")
            if max_amount:
                query = query.filter(Transaction.amount <= float(max_amount))

            # 🟦 order_by
            order_by = filters.get("order_by", "created_at")
            if hasattr(Transaction, order_by):
                column = getattr(Transaction, order_by)
                query = query.order_by(column.desc())
            else:
                 query = query.order_by(Transaction.created_at.desc())

            # 🟦 paginação
            page = int(filters.get("page", 1))
            per_page = int(filters.get("per_page", 20))
            offset = (page - 1) * per_page

            query = query.offset(offset).limit(per_page)

            # Executa
            results = query.all()
            return [t.as_dict for t in results]

        finally:
            db.close()
