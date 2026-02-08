def test_login_success(client, test_user):
    res = client.post("/auth/login", json={
        "email": test_user.email,
        "password": "123456"
    })

    assert res.status_code == 200
    data = res.get_json()
    assert "access_token" in data

def test_login_invalid_password(client, test_user):
    res = client.post("/auth/login", json={
        "email": test_user.email,
        "password": "wrong"
    })

    assert res.status_code == 401

def test_login_user_not_found(client):
    res = client.post("/auth/login", json={
        "email": "notfound@mail.com",
        "password": "123456"
    })

    assert res.status_code == 401

def test_protected_route_requires_auth(client):
    res = client.get("/transactions/")
    assert res.status_code == 401

def test_auth_me_without_token(client):
    res = client.get("/auth/me")
    assert res.status_code == 401

def test_protected_route_with_auth(client, auth_headers):
    res = client.get("/transactions/", headers=auth_headers)

    assert res.status_code == 200

def test_auth_me(client, auth_headers):
    res = client.get("/auth/me", headers=auth_headers)

    assert res.status_code == 200
    data = res.get_json()

    assert data["user_id"] is not None
    assert "name" in data
    assert "email" in data

def test_auth_me_invalid_token(client):
    res = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer token_invalido"}
    )

    assert res.status_code == 401
