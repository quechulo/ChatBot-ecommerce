import pytest
from app import create_app
from app.dbReader import get_connection_reader, access_db_collection

@pytest.fixture(scope="module")
def mongodb_connection():
    client = get_connection_reader()
    collection = access_db_collection(client, 'products', 'shoes')
    yield client, collection
    client.close()


def test_mongodb_connection(mongodb_connection):
    client, collection = mongodb_connection
    assert client is not None
    assert collection is not None
