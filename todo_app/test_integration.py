import os
import pytest
import requests
from todo_app import create_app
from dotenv import load_dotenv, find_dotenv

# NOT FINISHED
@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    # Create the new app.
    test_app = create_app.create_app()

    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client

class StubResponse():
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data

    def json(self):
        return self.fake_response_data

# Stub replacement for requests.get(url)
def stub(url, params={}):
    test_board_id = os.environ.get('BOARD_ID')
    fake_response_data = None
    if url == f'https://api.trello.com/1/boards/{test_board_id}/lists':
        fake_response_data = [{
            'id': '123abc',
            'name': 'To Do',
            'cards': [{'id': '456', 'name': 'Test card'}]
        }]
        return StubResponse(fake_response_data)
    list_id = '123abc'
    if url == f'https://api.trello.com/1/list/{list_id}/cards':
        fake_response_data_1 = [{
            'id': 'card1',
            'name': 'Test card',
            'desc': 'Test',
            'badges': {'due': '2022-07-22'}
        }]
        return StubResponse(fake_response_data_1)

    raise Exception(f'Integration test did not expect URL "{url}"')


def test_index_page(monkeypatch, client):
    # Replace requests.get(url) with our own function
    monkeypatch.setattr(requests, 'get', stub)

    # Make a request to our app's index page
    response = client.get('/')

    assert response.status_code == 200
    assert 'Test card' in response.data.decode()

