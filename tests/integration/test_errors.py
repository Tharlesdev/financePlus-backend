
def test_404_not_found(client):
    res = client.get("/rota-que-nao-existe")
    assert res.status_code == 404
    data = res.get_json()
    assert data["error"] == "Recurso não encontrado"

def test_validation_error(client, auth_headers):
    # Enviar JSON inválido para criar transação (falta campo obrigatório)
    res = client.post(
        "/transactions/",
        headers=auth_headers,
        json={
            "description": "Missing amount",
            # "amount": 100, # Faltando
            "type": "expense",
            "category_id": "uuid-fake"
        }
    )
    
    # Deve retornar 400 com formato padrão
    assert res.status_code == 400
    data = res.get_json()
    assert data["error"] == "Dados inválidos"
    assert isinstance(data["details"], list)
