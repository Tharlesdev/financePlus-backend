import pytest
from src.app.externals.models.category import Category

def test_create_category_success(client, auth_headers):
    data = {
        "name": "Alimentação"
    }
    response = client.post("/categories/", json=data, headers=auth_headers)
    assert response.status_code == 201
    assert response.json["name"] == "Alimentação"
    assert "id" in response.json

def test_list_categories_success(client, auth_headers):
    # Criar uma categoria primeiro
    client.post("/categories/", json={"name": "Lazer"}, headers=auth_headers)
    
    response = client.get("/categories/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) >= 1

def test_get_category_by_id(client, auth_headers):
    create_resp = client.post("/categories/", json={"name": "Saúde"}, headers=auth_headers)
    category_id = create_resp.json["id"]
    
    response = client.get(f"/categories/{category_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json["name"] == "Saúde"

def test_update_category(client, auth_headers):
    create_resp = client.post("/categories/", json={"name": "Transporte"}, headers=auth_headers)
    category_id = create_resp.json["id"]
    
    update_data = {"name": "Transporte Público"}
    response = client.put(f"/categories/{category_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    assert response.json["name"] == "Transporte Público"

def test_delete_category(client, auth_headers):
    create_resp = client.post("/categories/", json={"name": "Outros"}, headers=auth_headers)
    category_id = create_resp.json["id"]
    
    response = client.delete(f"/categories/{category_id}", headers=auth_headers)
    assert response.status_code == 200
    
    # Verificar se foi deletado
    get_resp = client.get(f"/categories/{category_id}", headers=auth_headers)
    assert get_resp.status_code == 404
