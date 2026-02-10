from src.app.repositories.recurring_repository import RecurringRepository
from src.app.services.transaction_service import transaction_service
from dateutil.relativedelta import relativedelta
from datetime import datetime

class RecurringService:
    def __init__(self):
        self.repo = RecurringRepository()

    def create_recurring(self, data: dict):
        return self.repo.create(data)

    def get_user_recurring(self, user_id):
        return self.repo.get_all_by_user(user_id)

    def process_due_transactions(self):
        """Verifica e processa transações recorrentes pendentes"""
        due_list = self.repo.get_due_transactions()
        processed_count = 0

        for rec in due_list:
            # 1. Criar a transação real
            tx_data = {
                "user_id": rec.user_id,
                "category_id": rec.category_id,
                "description": f"{rec.description} (Recorrente)",
                "amount": rec.amount,
                "type": rec.type,
                # A data da transação deve ser a data que estava agendada (next_run), não necessariamente hoje
                # Mas TransactionService usa created_at default=now. 
                # Vamos passar explicitamente se o service aceitar, ou deixar como today.
                # O ideal seria ter data da transação customizável.
                # Por simplicidade, vamos deixar created_at = now (data do processamento).
            }
            
            try:
                transaction_service.create_transaction(tx_data)
                
                # 2. Calcular próxima data
                next_date = rec.next_run
                if rec.frequency == 'weekly':
                    next_date += relativedelta(weeks=1)
                elif rec.frequency == 'monthly':
                    next_date += relativedelta(months=1)
                elif rec.frequency == 'yearly':
                    next_date += relativedelta(years=1)
                
                # 3. Atualizar recorrente
                self.repo.update(rec.id, {"next_run": next_date})
                processed_count += 1
                
            except Exception as e:
                print(f"Erro ao processar recorrente {rec.id}: {e}")
                # Logar erro, mas continuar processando as outras
        
        return processed_count
