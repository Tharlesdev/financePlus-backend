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
             # Para simplificar refatoração sem mudar controller, vamos retornar erro formatado se for o caso,
             # mas o ideal é o Controller validar.
             # Como o Repository retorna [], o Controller vai retornar [] 200 OK se não tiver user_id?
             # Vamos ver o controller.
             return {"error": "user_id é obrigatório"}, 400
        
        # O Repository retorna a lista diretamente.
        return self.repo.list(filters)

transaction_service = TransactionService()
