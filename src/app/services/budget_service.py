from src.app.repositories.budget_repository import BudgetRepository
from src.app.repositories.transaction_repository import TransactionRepository
from datetime import datetime
import calendar

class BudgetService:
    def __init__(self):
        self.repo = BudgetRepository()
        self.tx_repo = TransactionRepository()

    def create_budget(self, data: dict):
        return self.repo.create(data)

    def get_budgets_status(self, user_id, month: str):
        # 1. Buscar todos os budgets do usuário para o mês
        budgets = self.repo.get_by_user_and_month(user_id, month)
        
        # 2. Para cada budget, calcular o gasto real
        result = []
        
        # Define start/end date do mês
        year, m = map(int, month.split('-'))
        start_date = datetime(year, m, 1)
        last_day = calendar.monthrange(year, m)[1]
        end_date = datetime(year, m, last_day, 23, 59, 59)

        for budget in budgets:
            # Filtros para pegar transações da categoria neste mês
            filters = {
                "user_id": user_id,
                "category_id": budget.category_id,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "type": "expense" # Budgets geralmente são para despesas
            }
            
            # Precisamos somar o total. O repo.list retorna lista e total count, mas não soma.
            # Vamos pegar a lista e somar no python (ou criar método específico no repo se ficar lento)
            transactions, _ = self.tx_repo.list(filters)
            spent = float(sum(t["amount"] for t in transactions))
            
            b_dict = {
                "id": budget.id,
                "user_id": budget.user_id,
                "category_id": budget.category_id,
                "amount": budget.amount,
                "month": budget.month,
                "created_at": budget.created_at,
                "spent": spent,
                "remaining": budget.amount - spent,
                "percentage": (spent / budget.amount) * 100 if budget.amount > 0 else 0
            }
            result.append(b_dict)
            
        return result

    def delete_budget(self, budget_id):
        return self.repo.delete(budget_id)
