def _read(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def test_update_profile_endpoint_checks_auth_and_patches():
    content = _read('apis/authentication/3910135_auth_update_profile_app_PATCH.xs')
    assert 'query "auth/update_profile_app"' in content
    assert 'auth = "user"' in content
    assert 'db.patch user' in content
    assert '$auth.id' in content
    assert 'filter_empty_text' in content


def test_request_reset_endpoint_saves_token():
    content = _read('apis/authentication/3910136_auth_request_password_reset_app_POST.xs')
    assert 'query "auth/request_password_reset_app"' in content
    assert 'db.patch user' in content
    assert 'password_reset' in content
    assert 'token' in content
    assert 'expiration' in content


def test_reset_password_endpoint_verifies_token_and_patches():
    content = _read('apis/authentication/3910137_auth_reset_password_app_POST.xs')
    assert 'query "auth/reset_password_app"' in content
    assert 'security.check_password' in content
    assert 'password_reset.used == false' in content
    assert 'db.patch user' in content
