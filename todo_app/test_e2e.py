import os
import pytest
from threading import Thread
from time import sleep
from selenium import webdriver
from dotenv import load_dotenv
from todo_app import create_app
from selenium.webdriver.firefox.options import Options
import requests

@pytest.fixture(scope='module')
def app_with_temp_board():
    # Load our real environment variables
    load_dotenv(override=True)

    # Create the new board & update the board id environment variable
    board_id = create_trello_board()
    os.environ['BOARD_ID'] = board_id

    # Construct the new application
    application = create_app.create_app()

    # Start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()

    # Give the app a moment to start
    sleep(1)

    # Return the application object as the result of the fixture
    yield application

    # Tear down
    thread.join(1)
    delete_trello_board(board_id)


def create_trello_board():
    # TODO Create a new board in Trello and return the id
    url = f"https://api.trello.com/1/boards/?name=E2ETest&key={os.getenv('KEY')}&token={os.getenv('TOKEN')}&idOrganization=userworkspace30763063&prefs_permissionLevel=public"
    r = requests.post(url).json()
    return r['id']


def delete_trello_board(board_id):
    # TODO Delete the Trello board with id board_id
    url = "https://api.trello.com/1/boards/" + board_id
    parameters = {'key': os.getenv('KEY'), 'token': os.getenv('TOKEN')}
    r = requests.delete(url, params=parameters)


@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    with webdriver.Firefox(options=options) as driver:
        yield driver


def test_task_journey(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')

    assert driver.title == 'To-Do App'

