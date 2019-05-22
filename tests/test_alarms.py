from elmo.api.exceptions import APIException, PermissionDenied


def test_alarms_wrong_mimetype(client):
    """Should return 415 if JSON is not used"""
    result = client.simulate_put(
        "/api/v0/alarms",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Bearer 127d9a48-927a-43f3-a3e3-842f3f2b7393",
        },
        body="code=1234567890",
    )
    assert result.status_code == 415


def test_alarm_missing_code(client):
    """Should return 400 if the code is missing from the payload"""
    result = client.simulate_put(
        "/api/v0/alarms",
        headers={"Authorization": "Bearer 127d9a48-927a-43f3-a3e3-842f3f2b7393"},
        json={},
    )
    assert result.status_code == 400


def test_alarm_successful_armed(mocker, client):
    """Should return 200 if all alarms have been activated"""
    mock = mocker.patch("server.resources.ElmoClient")
    instance = mock.return_value

    result = client.simulate_put(
        "/api/v0/alarms",
        headers={"Authorization": "Bearer 127d9a48-927a-43f3-a3e3-842f3f2b7393"},
        json={"code": "1234567890"},
    )
    instance.lock.assert_called_once_with("1234567890")
    assert instance.arm.call_count == 1
    assert instance._session_id == "127d9a48-927a-43f3-a3e3-842f3f2b7393"
    assert result.status_code == 200
    assert result.json == {"alarms_armed": True}


def test_alarm_invalid_expired_token(mocker, client):
    """Should return 200 if all alarms have been activated"""
    mocker.patch("server.resources.ElmoClient.lock", side_effect=PermissionDenied)

    result = client.simulate_put(
        "/api/v0/alarms",
        headers={"Authorization": "Bearer 127d9a48-927a-43f3-a3e3-842f3f2b7393"},
        json={"code": "1234567890"},
    )
    assert result.status_code == 401


def test_alarm_api_exception(mocker, client):
    """Should return 200 if all alarms have been activated"""
    mocker.patch("server.resources.ElmoClient.lock", side_effect=APIException)

    result = client.simulate_put(
        "/api/v0/alarms",
        headers={"Authorization": "Bearer 127d9a48-927a-43f3-a3e3-842f3f2b7393"},
        json={"code": "1234567890"},
    )
    assert result.status_code == 503


def test_disarm_wrong_mimetype(client):
    """Should return 415 if JSON is not used"""
    result = client.simulate_delete(
        "/api/v0/alarms",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Bearer 127d9a48-927a-43f3-a3e3-842f3f2b7393",
        },
        body="code=1234567890",
    )
    assert result.status_code == 415


def test_disarm_missing_code(client):
    """Should return 400 if the code is missing from the payload"""
    result = client.simulate_delete(
        "/api/v0/alarms",
        headers={"Authorization": "Bearer 127d9a48-927a-43f3-a3e3-842f3f2b7393"},
        json={},
    )
    assert result.status_code == 400


def test_disarm_successful_armed(mocker, client):
    """Should return 200 if all alarms have been activated"""
    mock = mocker.patch("server.resources.ElmoClient")
    instance = mock.return_value

    result = client.simulate_delete(
        "/api/v0/alarms",
        headers={"Authorization": "Bearer 127d9a48-927a-43f3-a3e3-842f3f2b7393"},
        json={"code": "1234567890"},
    )
    instance.lock.assert_called_once_with("1234567890")
    assert instance.disarm.call_count == 1
    assert instance._session_id == "127d9a48-927a-43f3-a3e3-842f3f2b7393"
    assert result.status_code == 200
    assert result.json == {"alarms_armed": False}


def test_disarm_invalid_expired_token(mocker, client):
    """Should return 200 if all alarms have been activated"""
    mocker.patch("server.resources.ElmoClient.lock", side_effect=PermissionDenied)

    result = client.simulate_delete(
        "/api/v0/alarms",
        headers={"Authorization": "Bearer 127d9a48-927a-43f3-a3e3-842f3f2b7393"},
        json={"code": "1234567890"},
    )
    assert result.status_code == 401


def test_disarm_api_exception(mocker, client):
    """Should return 200 if all alarms have been activated"""
    mocker.patch("server.resources.ElmoClient.lock", side_effect=APIException)

    result = client.simulate_delete(
        "/api/v0/alarms",
        headers={"Authorization": "Bearer 127d9a48-927a-43f3-a3e3-842f3f2b7393"},
        json={"code": "1234567890"},
    )
    assert result.status_code == 503
