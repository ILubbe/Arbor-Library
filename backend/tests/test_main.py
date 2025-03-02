import pytest, json
from app import app
from config import db
from tests.test_cases import *

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# helpers
def librian_tokens(client):
    response = client.post('/login', json={"email": librarian_email, "password": librarian_password})
    assert response.status_code == 200
    return {
        "access_token": response.get_json()['accessToken'],
        "refresh_token": response.get_json()['refreshToken']
    }

def patron_tokens(client):
    response = client.post('/login', json={"email": patron_email, "password": patron_password})
    assert response.status_code == 200
    return {
        "access_token": response.get_json()['accessToken'],
        "refresh_token": response.get_json()['refreshToken']
    }

def add_headers(client, role, token_type):
    if role == "librarian":
        if token_type == "access":
            return {"Authorization": f"Bearer {librian_tokens(client)['access_token']}"}
        elif token_type == "refresh":
            return {"Authorization": f"Bearer {librian_tokens(client)['refresh_token']}"}
            
    elif role == "patron":
        if token_type == "access":
            return {"Authorization": f"Bearer {patron_tokens(client)['access_token']}"}
        elif token_type == "refresh":
            return {"Authorization": f"Bearer {patron_tokens(client)['refresh_token']}"}

# tests
# create user
@pytest.mark.parametrize("email, password, passwordConfirmation, firstName, lastName, expected_status", create_user_test_cases)
def test_create_user(client, email, password, passwordConfirmation, firstName, lastName, expected_status):
    response = client.post('/users', json={"email": email, "password": password, "passwordConfirmation": passwordConfirmation, "firstName": firstName, "lastName": lastName})
    assert response.status_code == expected_status

# login
@pytest.mark.parametrize("email, password, expected_status", login_test_cases)
def test_login(client, email, password, expected_status):
    response = client.post('/login', json={"email": email, "password": password})
    assert response.status_code == expected_status

# refresh
@pytest.mark.parametrize("role, expected_status", refresh_test_cases)
def test_login(client, role, expected_status):
    headers = add_headers(client, role, "refresh")
    response = client.post("/refresh", headers=headers)
    assert response.status_code == expected_status

# logout
@pytest.mark.parametrize("role, expected_status", logout_test_cases)
def test_login(client, role, expected_status):
    headers = add_headers(client, role, "refresh")
    response = client.post("/logout", headers=headers)
    assert response.status_code == expected_status

# get endpoints
@pytest.mark.parametrize("endpoint, role, args, expected_status", get_endpoints_test_cases)
def test_get_endpoints(client, endpoint, role, args, expected_status):
    headers = add_headers(client, role, "access")
    response = client.get(f'{endpoint}{args}', headers=headers)
    assert response.status_code == expected_status

# post endpoints
@pytest.mark.parametrize("endpoint, role, args, body, expected_status", post_endpoints_test_cases)
def test_post_endpoints(client, endpoint, role, args, body, expected_status):
    headers = add_headers(client, role, "access")
    response = client.post(f'{endpoint}{args}', headers=headers, json=body)
    assert response.status_code == expected_status

# put endpoints
@pytest.mark.parametrize("endpoint, role, args, body, expected_status", put_endpoints_test_cases)
def test_put_endpoints(client, endpoint, role, args, body, expected_status):
    headers = add_headers(client, role, "access")
    response = client.put(f'{endpoint}{args}', headers=headers, json=body)
    assert response.status_code == expected_status

# delete endpoints
@pytest.mark.parametrize("endpoint, role, args, expected_status", delete_endpoints_test_cases)
def test_delete_endpoints(client, endpoint, role, args, expected_status):
    headers = add_headers(client, role, "access")
    response = client.delete(f'{endpoint}{args}', headers=headers)
    assert response.status_code == expected_status

# patch endpoints
@pytest.mark.parametrize("endpoint, role, args, body, expected_status", patch_endpoints_test_cases)
def test_patch_endpoints(client, endpoint, role, args, body, expected_status):
    headers = add_headers(client, role, "access")
    response = client.patch(f'{endpoint}{args}', headers=headers, json=body)
    assert response.status_code == expected_status
