from src.app.repositories.dashboard_repository import DashboardRepository

class DashboardService:
    def __init__(self):
        self.repo = DashboardRepository()

    def get_dashboard_data(self, user_id):
        # 1. Monthly Balance
        raw_monthly = self.repo.get_monthly_summary(user_id)
        # raw_monthly is list of (month, type, total)
        
        monthly_map = {}
        for month, type_, total in raw_monthly:
            if month not in monthly_map:
                monthly_map[month] = {"income": 0, "expense": 0}
            
            t_lower = type_.lower()
            if t_lower in ["income", "receita", "entrada"]:
                 monthly_map[month]["income"] += float(total)
            elif t_lower in ["expense", "despesa", "saida", "saída"]:
                 monthly_map[month]["expense"] += float(total)
        
        monthly_data = []
        for month in sorted(monthly_map.keys()):
            m = monthly_map[month]
            balance = m["income"] - m["expense"]
            monthly_data.append({
                "month": month,
                "income": m["income"],
                "expense": m["expense"],
                "balance": balance
            })

        # 2. Category Expenses (Top categories)
        # Note: Repository currently filters by 'expense'.
        raw_categories = self.repo.get_category_expenses(user_id)
        category_data = [
            {"category": name, "total": float(total)}
            for name, total in raw_categories
        ]

        # 3. Insights
        total_income = sum(item["income"] for item in monthly_data)
        total_expense = sum(item["expense"] for item in monthly_data)
        current_balance = total_income - total_expense
        
        top_category = category_data[0]["category"] if category_data else "N/A"
        
        # Savings Rate
        savings_rate = 0
        if total_income > 0:
            savings_rate = ((total_income - total_expense) / total_income) * 100

        insights = {
            "total_income": total_income,
            "total_expense": total_expense,
            "current_balance": current_balance,
            "savings_rate": round(savings_rate, 2),
            "top_expense_category": top_category
        }

        return {
            "monthly_balance": monthly_data,
            "expenses_by_category": category_data,
            "insights": insights
        }

dashboard_service = DashboardService()
