import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app(testing=True)
    with app.test_client() as client:
        yield client

def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the BuyStuff Chatbot's API" in response.data

def test_messages_list(client):
    response = client.get('/receive')
    assert response.status_code == 200
    assert b'{"messages":[]}\n' in response.data

def test_fresh_conversation(client):
    response = client.get('/fresh-conversation')
    assert response.status_code == 200
    assert b'{"status":"Chatbot context was restarted"}\n' in response.data
