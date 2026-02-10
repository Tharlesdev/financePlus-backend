import pytest

def test_export_endpoints(client, auth_headers):
    # 1. Create some data
    cat_res = client.post("/categories/", json={"name": "Export Cat", "type": "expense"}, headers=auth_headers)
    cat_id = cat_res.json["id"]
    
    client.post("/transactions/", json={
        "category_id": cat_id,
        "amount": 100.0,
        "description": "Export Item 1",
        "date": "2023-10-01",
        "type": "expense"
    }, headers=auth_headers)

    # 2. Test CSV
    res = client.get("/transactions/export/csv", headers=auth_headers)
    assert res.status_code == 200
    assert "text/csv" in res.headers["Content-Type"]
    assert "Export Item 1" in res.text

    # 3. Test Excel
    res = client.get("/transactions/export/excel", headers=auth_headers)
    assert res.status_code == 200
    assert "spreadsheetml.sheet" in res.headers["Content-Type"]
    assert len(res.data) > 0
