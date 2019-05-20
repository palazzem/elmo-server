from elmo.api.exceptions import APIException, PermissionDenied


def test_endpoint_wrong_mimetype(client):
    """Should return 415 if JSON is not used"""
    result = client.simulate_post(
        "/api/v0/auth",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        body="username=test&password=test",
    )
    assert result.status_code == 415


def test_auth_missing_username_password(client):
    """Should return 400 if username or password are missing"""
    result = client.simulate_post("/api/v0/auth", json={})
    assert result.status_code == 400
    result = client.simulate_post("/api/v0/auth", json={"username": "test"})
    assert result.status_code == 400
    result = client.simulate_post("/api/v0/auth", json={"password": "test"})
    assert result.status_code == 400


def test_auth_successful_authentication(mocker, client):
    """Should return 200 and an access token if the authentication is successful"""
    mocker.patch("server.resources.ElmoClient.auth", return_value="token")

    result = client.simulate_post(
        "/api/v0/auth", json={"username": "test", "password": "test"}
    )
    assert result.status_code == 200
    assert result.json == {"access_token": "token"}


def test_auth_permission_denied(mocker, client):
    """Should return 403 if credentials are wrong"""
    mocker.patch("server.resources.ElmoClient.auth", side_effect=PermissionDenied)

    result = client.simulate_post(
        "/api/v0/auth", json={"username": "test", "password": "test"}
    )
    assert result.status_code == 403


def test_auth_server_error(mocker, client):
    """Should return 503 if Elmo API is unavailable"""
    mocker.patch("server.resources.ElmoClient.auth", side_effect=APIException)

    result = client.simulate_post(
        "/api/v0/auth", json={"username": "test", "password": "test"}
    )
    assert result.status_code == 503
