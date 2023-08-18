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


def test_send_fresh_message(client):
    response = client.post('/send-fresh', json={'message': 'Szukam butów', 'sender': 'user', 'userEmail': 'test@test.com'})
    assert response.status_code == 200
    assert response.json['query'] == 'Szukam butów'
    assert response.json['answer'] is not None
    assert 'but' in response.json['answer']
    assert 'http' in response.json['link']
    assert response.json['sender'] is not None


def test_send_fresh_message_about(client):
    response = client.post('/send-fresh', json={'message': 'Na jaki adres email można składać reklamacje?', 'sender': 'user', 'userEmail': 'test@test.com'})
    assert response.status_code == 200
    assert response.json['query'] == 'Na jaki adres email można składać reklamacje?'
    assert response.json['answer'] is not None
    assert 'bok@buystuff.pl' in response.json['answer']
    assert 'http' in response.json['link']
    assert response.json['sender'] is not None


def test_send_message_about(client):
    response = client.post('/send', json={'message': 'Ile mam dni na darmowy zwrot?', 'sender': 'user', 'userEmail': 'test@test.com'})
    assert response.status_code == 200
    assert response.json['query'] == 'Ile mam dni na darmowy zwrot?'
    assert response.json['answer'] is not None
    assert response.json['link'] is not None


# Tests for request without proper structure
def test_send_fresh_message_with_no_message(client):
    response = client.post('/send-fresh', json={'sender': 'user', 'userEmail': 'test@test.com'})
    assert response.status_code == 400

def test_send_message_with_no_message(client):
    response = client.post('/send', json={'sender': 'user', 'userEmail': 'test@test.com'})
    assert response.status_code == 400

def test_send_fresh_message_with_no_sender(client):
    response = client.post('/send-fresh', json={'message': 'Hello', 'userEmail': 'test@test.com'})
    assert response.status_code == 400

def test_send_message_with_no_sender(client):
    response = client.post('/send', json={'message': 'Hello', 'userEmail': 'test@test.com'})
    assert response.status_code == 400

def test_send_fresh_message_with_no_user_email(client):
    response = client.post('/send-fresh', json={'message': 'Hello', 'sender': 'user'})
    assert response.status_code == 400
