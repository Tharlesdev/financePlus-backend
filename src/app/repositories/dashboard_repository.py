from sqlalchemy import func, extract
from src.app.externals.db.connection import SessionLocal
from src.app.externals.models.transaction import Transaction
from src.app.externals.models.category import Category
from uuid import UUID

class DashboardRepository:
    def get_monthly_summary(self, user_id):
        session = SessionLocal()
        try:
            # Agrupa por ano e mês
            # SQLite: strftime('%Y-%m', created_at)
            # SQLAlchemy genérico: extract('year', ...), extract('month', ...)
            # Vamos usar strftime para SQLite pois é o padrão atual
            
            if isinstance(user_id, str):
                user_id = UUID(user_id)
                
            query = session.query(
                func.strftime('%Y-%m', Transaction.created_at).label('month'),
                Transaction.type,
                func.sum(Transaction.amount).label('total')
            ).filter(
                Transaction.user_id == user_id
            ).group_by(
                'month', Transaction.type
            ).order_by(
                'month'
            )
            
            return query.all()
        finally:
            session.close()

    def get_category_expenses(self, user_id):
        session = SessionLocal()
        try:
            if isinstance(user_id, str):
                user_id = UUID(user_id)

            query = session.query(
                Category.name,
                func.sum(Transaction.amount).label('total')
            ).join(
                Transaction, Transaction.category_id == Category.id
            ).filter(
                Transaction.user_id == user_id,
                func.lower(Transaction.type).in_(['expense', 'despesa', 'saída', 'saida'])
            ).group_by(
                Category.name
            ).order_by(
                func.sum(Transaction.amount).desc()
            )
            
            return query.all()
        finally:
            session.close()
