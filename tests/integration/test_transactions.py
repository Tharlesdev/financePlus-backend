def test_create_transaction_success(client, auth_headers):
    # cria categoria
    cat_res = client.post(
        "/categories/",
        headers=auth_headers,
        json={"name": "Salary"}
    )

    category_id = cat_res.get_json()["id"]

    # cria transação
    res = client.post(
        "/transactions/",
        headers=auth_headers,
        json={
            "description": "Salary",
            "amount": 5000,
            "type": "income",
            "category_id": category_id
        }
    )

    assert res.status_code == 201
    data = res.get_json()
    assert data["description"] == "Salary"


def test_list_transactions_without_auth(client):
    res = client.get("/transactions/")

    assert res.status_code == 401


def test_list_transactions_without_auth(client):
    res = client.get("/transactions/")

    assert res.status_code == 401

def test_list_transactions_with_auth_empty(client, auth_headers):
    res = client.get("/transactions/", headers=auth_headers)

    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list)
    assert len(data) == 0

def test_list_transactions(client, auth_headers):
    # 1️⃣ cria categoria
    cat_res = client.post(
        "/categories/",
        headers=auth_headers,
        json={"name": "Salary"}
    )
    assert cat_res.status_code == 201
    category_id = cat_res.get_json()["id"]

    # 2️⃣ cria transação
    tx_res = client.post(
        "/transactions/",
        headers=auth_headers,
        json={
            "description": "Salary",
            "amount": 5000,
            "type": "income",
            "category_id": category_id
        }
    )
    assert tx_res.status_code == 201

    # 3️⃣ lista transações
    res = client.get(
        "/transactions/",
        headers=auth_headers
    )

    assert res.status_code == 200
    data = res.get_json()

    assert len(data) == 1
    assert data[0]["description"] == "Salary"


