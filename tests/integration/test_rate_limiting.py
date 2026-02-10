
import pytest
from src.app.app import create_app

@pytest.fixture
def app_with_limiter():
    app = create_app()
    app.config["TESTING"] = True
    app.config["RATELIMIT_ENABLED"] = True  # Força o limiter a funcionar nos testes
    app.config["RATELIMIT_STORAGE_URI"] = "memory://"
    return app

@pytest.fixture
def client_limiter(app_with_limiter):
    return app_with_limiter.test_client()

def test_rate_limit_login(client_limiter):
    # O limite configurado é "10 per minute" para /auth/login
    
    # Faz 10 requisições permitidas
    for i in range(10):
        res = client_limiter.post("/auth/login", json={
            "email": "wrong@email.com",
            "password": "wrong"
        })
        # Pode retornar 401 (falha login) ou 200 (se existisse), mas não 429
        assert res.status_code != 429

    # A 11ª deve ser bloqueada
    res = client_limiter.post("/auth/login", json={
        "email": "wrong@email.com",
        "password": "wrong"
    })
    
    assert res.status_code == 429
    data = res.get_json()
    assert "error" in data
    # assert "ratelimit exceeded" in data["error"].lower()
    # A mensagem padrão do limiter é "10 per 1 minute"
    assert "10 per 1 minute" in data["error"]
