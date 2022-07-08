from flask import Flask, render_template, redirect, request, url_for

from todo_app.flask_config import Config
from todo_app.data.session_items import get_items, add_item, save_item, remove_item

app = Flask(__name__)
app.config.from_object(Config())

@app.route('/')
def index():
    return render_template('index.html', listOfItems=get_items())

@app.route('/', methods=['POST'])
def add():
    title = request.form.get('title')
    if request.form.get('option') == "add":
        add_item(title)
    elif request.form.get('option') == 'start':
        x = get_info(title)
        new_item = {'id': x.id, 'title': title, 'status': 'Started'}
        save_item(new_item)
    elif request.form.get('option') == 'complete':
        x = get_info(title)
        new_item = { 'id': x.id, 'title': title, 'status': 'Completed' }
        save_item(new_item)
    elif request.form.get('option') == 'delete':
        remove_item(title)
    return redirect(url_for('index'))


def get_info(title):
    for item in get_items():
        if item.title == title:
            return item
