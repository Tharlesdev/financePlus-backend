import pandas as pd
from io import BytesIO
from src.app.services.transaction_service import transaction_service

class ExportService:
    def export_transactions_csv(self, filters: dict):
        # 1. Buscar dados
        # Forçamos paginação alta para pegar tudo
        filters["per_page"] = 100000 
        filters["page"] = 1
        
        result = transaction_service.list(filters)
        transactions = result["data"] # Lista de dicts
        
        if not transactions:
            return None

        # 2. Criar DataFrame
        df = pd.DataFrame(transactions)
        
        # Selecionar e renomear colunas amigáveis
        # Assumindo que transactions tem chaves do modelo
        cols = ["created_at", "description", "amount", "type", "category"] 
        # Ajuste conforme o dict retornado pelo as_dict do model
        
        # Se 'category' for objeto/dict, precisamos extrair o nome
        if "category" in df.columns:
            df["category_name"] = df["category"].apply(lambda x: x.get("name") if isinstance(x, dict) else str(x))
        else:
            df["category_name"] = "N/A"

        final_df = df[["created_at", "description", "amount", "type", "category_name"]]
        final_df.columns = ["Data", "Descrição", "Valor", "Tipo", "Categoria"]

        # 3. Gerar CSV
        output = BytesIO()
        final_df.to_csv(output, index=False, encoding='utf-8-sig') # utf-8-sig para Excel abrir com acentos
        output.seek(0)
        return output

    def export_transactions_excel(self, filters: dict):
        # Mesmo processo, output Excel
        filters["per_page"] = 100000 
        filters["page"] = 1
        
        result = transaction_service.list(filters)
        transactions = result["data"]
        
        if not transactions:
            return None

        df = pd.DataFrame(transactions)
        
        if "category" in df.columns:
            df["category_name"] = df["category"].apply(lambda x: x.get("name") if isinstance(x, dict) else str(x))
        else:
            df["category_name"] = "N/A"
            
        final_df = df[["created_at", "description", "amount", "type", "category_name"]]
        final_df.columns = ["Data", "Descrição", "Valor", "Tipo", "Categoria"]

        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            final_df.to_excel(writer, index=False, sheet_name='Transações')
        
        output.seek(0)
        return output
