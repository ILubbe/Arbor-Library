import pytest, json
from backend.main import app

#sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# GET
def test_get(client):
    response = client.get('/users/')
    print(response.json)
    assert response.status_code == 200
"""
# clean up the users below if any were made
test_users_to_be_created = [
    "testuser",
    "shortpass",
    "nospecialchars",
    "missingfield"
]
@pytest.fixture
def cleanup_testusers(test_users_to):

# POST
@pytest.mark.parametrize(
    "payload, expected_status", [
        # Successful creation
        (
            {
                "role": "patron",
                "username": "testuser",
                "password": "StrongP@ssw0rd!",
                "passwordConfirmation": "StrongP@ssw0rd!",
                "firstName": "John",
                "lastName": "Doe"
            },
            201
        ),
        
        # Password too short
        (
            {
                "role": "patron",
                "username": "shortpass",
                "password": "short",
                "passwordConfirmation": "short",
                "firstName": "John",
                "lastName": "Doe"
            },
            400
        ),
        
        # Password missing special character
        (
            {
                "role": "patron",
                "username": "nospecialchars",
                "password": "NoSpecial123",
                "passwordConfirmation": "NoSpecial123",
                "firstName": "John",
                "lastName": "Doe"
            },
            400
        ),
        
        # Username already taken
        (
            {
                "role": "patron",
                "username": "testuser", # depends on 1st payload's success
                "password": "ValidP@ssw0rd",
                "passwordConfirmation": "ValidP@ssw0rd",
                "firstName": "John",
                "lastName": "Doe"
            },
            400
        ),
        
        # Missing field
        (
            {
                "role": "patron",
                "username": "missingfield",
                "password": "ValidP@ssw0rd",
                "firstName": "John",
                "lastName": "Doe"
            },
            400,
        ),
    ]
)

def test_post(client, payload, expected_status):
    response = client.post('/users/', data=json.dumps(payload), content_type='application/json')
    assert response.status_code == expected_status

    # Check the database for successful creation in valid case
    if expected_status == 201:
        user_in_db = User.query.filter_by(username=payload["username"]).first()
        assert user_in_db is not None
        assert user_in_db.username == payload["username"]
"""