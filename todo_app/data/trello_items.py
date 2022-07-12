import requests
import os


class Item:
    def __init__(self, id, name, description, due, status='To Do'):
        self.id = id
        self.name = name
        self.description = description
        self.due = due
        self.status = status

    @classmethod
    def from_trello_card(cls, card, list):
        return cls(card['id'], card['name'], card['desc'], card['badges']['due'], list['name'])


cardsURL = "https://api.trello.com/1/cards/"
boardsURL = "https://api.trello.com/1/boards/"
listsURL = "https://api.trello.com/1/list/"


def get_parameters():
    return {'key': os.getenv('KEY'), 'token': os.getenv('TOKEN')}


def get_lists():
    return requests.get(boardsURL + os.getenv('BOARD_ID') + "/lists", params=get_parameters())


def get_cards_on_list(listID):
    return requests.get(listsURL + listID + '/cards', params=get_parameters())


def get_list_id(name):
    lists = get_lists().json()
    return next((list['id'] for list in lists if list['name'] == name), None)


def get_all_cards():
    lists = get_lists().json()
    itemList = []
    for list in lists:
        cards = get_cards_on_list(list.get('id')).json()
        for card in cards:
            itemList.append(Item.from_trello_card(card, list))
    return itemList


def add_card(title, desc, date):
    parameters = get_parameters()
    parameters.update({'idList': get_list_id('To Do'), 'name': title, 'desc': desc, 'due': date})
    return requests.post(cardsURL, params=parameters)


def start_card(cardID):
    parameters = get_parameters()
    parameters.update({'idList': get_list_id('Doing')})
    return requests.put(url=cardsURL + cardID, data=parameters)


def complete_card(cardID):
    parameters = get_parameters()
    parameters.update({'idList': get_list_id('Done')})
    return requests.put(url=cardsURL + cardID, data=parameters)


def redo_card(cardID):
    parameters = get_parameters()
    parameters.update({'idList': get_list_id('To Do')})
    return requests.put(url=cardsURL+cardID, data=parameters)


def delete_card(cardID):
    response = requests.request("DELETE", cardsURL+cardID, params=get_parameters())
    return response.text


def change_description(cardID, desc):
    parameters = get_parameters()
    parameters.update({'desc': desc})
    return requests.put(url=cardsURL+cardID, data=parameters)


def change_date(cardID, date):
    parameters = get_parameters()
    parameters.update({'due': date})
    return requests.put(url=cardsURL+cardID, data=parameters)
