import pytest
from datetime import date

def test_recurring_lifecycle(client, auth_headers):
    # 1. Create Category
    cat_res = client.post("/categories/", json={"name": "Recurring Cat", "type": "expense"}, headers=auth_headers)
    cat_id = cat_res.json["id"]

    # 2. Create Recurring Transaction
    # Use a past date to ensure it is "due" immediately
    data = {
        "category_id": cat_id,
        "description": "Netflix",
        "amount": 50.0,
        "type": "expense",
        "frequency": "monthly",
        "start_date": "2023-01-01" 
    }
    res = client.post("/recurring/", json=data, headers=auth_headers)
    assert res.status_code == 201
    rec_id = res.json["id"]

    # 3. List
    res = client.get("/recurring/", headers=auth_headers)
    assert res.status_code == 200
    assert len(res.json) >= 1
    
    # 4. Process (Manually trigger)
    proc_res = client.post("/recurring/process", headers=auth_headers)
    assert proc_res.status_code == 200
    assert proc_res.json["processed"] > 0
    
    # 5. Verify Transaction Created
    # Search for transactions with the description
    trans_res = client.get("/transactions/?description=Netflix", headers=auth_headers)
    assert trans_res.status_code == 200
    # Depending on pagination structure
    data = trans_res.json.get("data", trans_res.json) 
    assert len(data) > 0
    assert float(data[0]["amount"]) == 50.0
