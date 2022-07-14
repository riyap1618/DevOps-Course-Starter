from datetime import datetime
from todo_app.view_model import ViewModel
from todo_app.data.trello_items import Item

itemList = [
    Item(1, 'Test 1', 'test1', datetime(2022, 7, 20), 'To Do'),
    Item(2, 'Test 2', 'test2', datetime(2022, 7, 21), 'Doing'),
    Item(3, 'Test 3', 'test3', datetime(2022, 7, 22), 'Done'),
    Item(4, 'Test 4', 'test4', datetime(2022, 7, 23), 'Doing')
]

list = ViewModel(itemList)

def test_doing():
    # Act
    doingList = list.doing_items
    # Assert
    assert doingList == [itemList[1], itemList[3]]

def test_todo():
    # Arrange
    todoList = list.todo_items
    # Assert
    assert todoList == [itemList[0]]

def test_done():
    # Arrange
    doneList = list.done_items
    # Assert
    assert doneList == [itemList[2]]


