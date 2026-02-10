import pytest
from datetime import datetime

def test_create_and_get_budget(client, auth_headers):
    # 1. Create Category
    cat_res = client.post("/categories/", json={"name": "Budget Category", "type": "expense"}, headers=auth_headers)
    assert cat_res.status_code == 201
    cat_id = cat_res.json["id"]

    # 2. Create Budget
    month = datetime.now().strftime("%Y-%m")
    budget_data = {
        "category_id": cat_id,
        "amount": 1000.0,
        "month": month
    }
    res = client.post("/budgets/", json=budget_data, headers=auth_headers)
    assert res.status_code == 201
    assert res.json["amount"] == 1000.0

    # 3. Create Transaction to consume budget
    trans_data = {
        "category_id": cat_id,
        "amount": 200.0,
        "description": "Spending",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "type": "expense"
    }
    client.post("/transactions/", json=trans_data, headers=auth_headers)

    # 4. Get Budget Status
    res = client.get(f"/budgets/?month={month}", headers=auth_headers)
    assert res.status_code == 200
    data = res.json
    
    # Find our budget
    my_budget = next((b for b in data if b["category_id"] == cat_id), None)
    assert my_budget is not None
    assert my_budget["spent"] == 200.0
    assert my_budget["remaining"] == 800.0
    assert my_budget["percentage"] == 20.0

def test_delete_budget(client, auth_headers):
    # Setup category and budget
    cat_res = client.post("/categories/", json={"name": "Delete Budget Cat", "type": "expense"}, headers=auth_headers)
    cat_id = cat_res.json["id"]
    
    res = client.post("/budgets/", json={
        "category_id": cat_id,
        "amount": 500,
        "month": "2023-10"
    }, headers=auth_headers)
    budget_id = res.json["id"]
    
    # Delete
    del_res = client.delete(f"/budgets/{budget_id}", headers=auth_headers)
    assert del_res.status_code == 200
    
    # Verify deletion
    del_res = client.delete(f"/budgets/{budget_id}", headers=auth_headers)
    assert del_res.status_code == 404
