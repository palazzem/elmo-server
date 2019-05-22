def test_authorization_required(hooks_client):
    """Should return a 401 if the Authorization header is missing"""
    result = hooks_client.simulate_get("/hooks/authorization_required")
    assert result.status_code == 401


def test_authorization_is_valid(hooks_client):
    """Should return a 401 if the Authorization header doesn't contain a valid UUID"""
    headers = {"Authorization": "Test Token"}
    result = hooks_client.simulate_get("/hooks/authorization_required", headers=headers)
    assert result.status_code == 401


def test_authorization_is_valid_without_split(hooks_client):
    """Should return a 401 if the Authorization header doesn't contain a valid UUID"""
    headers = {"Authorization": "Token"}
    result = hooks_client.simulate_get("/hooks/authorization_required", headers=headers)
    assert result.status_code == 401


def test_authorization_success(hooks_client):
    """Should return a 401 if the Authorization header doesn't contain a valid UUID"""
    headers = {"Authorization": "Bearer 127d9a48-927a-43f3-a3e3-842f3f2b7393"}
    result = hooks_client.simulate_get("/hooks/authorization_required", headers=headers)
    assert result.status_code == 200
    assert result.json == {"token": "127d9a48-927a-43f3-a3e3-842f3f2b7393"}


def test_code_is_present(hooks_client):
    """Should return 200 if the code is present in the payload"""
    result = hooks_client.simulate_get(
        "/hooks/code_required", json={"code": "1234567890"}
    )
    assert result.status_code == 200
    assert result.json == {"code": "1234567890"}


def test_code_is_not_present(hooks_client):
    """Should return 400 if the code is missing from the payload"""
    result = hooks_client.simulate_get("/hooks/code_required", json={})
    assert result.status_code == 400
