from src.app.repositories.transaction_repository import TransactionRepository

class TransactionService:
    def __init__(self):
        self.repo = TransactionRepository()

    def create_transaction(self, data):
        return self.repo.create_transaction(data)

    def get_all_transactions(self):
        return self.repo.get_all_transactions()

    def get_transaction_by_id(self, transaction_id):
        return self.repo.get_transaction_by_id(transaction_id)

    def update_transaction(self, transaction_id, data):
        return self.repo.update_transaction(transaction_id, data)

    def delete_transaction(self, transaction_id):
        return self.repo.delete_transaction(transaction_id)

    def list(self, filters: dict):
        # Validação simples de user_id que estava no service antigo
        if not filters.get("user_id"):
             # O service antigo retornava erro 400. Vamos manter a consistência lançando exceção ou retornando erro.
             return {"error": "user_id é obrigatório"}, 400
        
        # O Repository retorna (dados, total)
        data, total_items = self.repo.list(filters)
        
        page = int(filters.get("page", 1))
        per_page = int(filters.get("per_page", 20))
        total_pages = (total_items + per_page - 1) // per_page
        
        return {
            "data": data,
            "meta": {
                "total_items": total_items,
                "total_pages": total_pages,
                "current_page": page,
                "per_page": per_page
            }
        }

transaction_service = TransactionService()
