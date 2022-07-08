from flask import Flask
from flask import render_template
from flask import redirect, request

from todo_app.flask_config import Config
from todo_app.data.session_items import get_items
from todo_app.data.session_items import add_item, save_item, remove_item

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    print(get_items())
    return render_template('index.html', listOfItems=get_items())
    #return 'Hello World!'

@app.route('/', methods=['POST'])
def add():
    if request.form.get('option') == "add":
        title = request.form.get('title')
        item = add_item(title)
    elif request.form.get('option') == 'start':
        title = request.form.get('title')
        for x in get_items():
            if x['title'] == title:
                new_item = { 'id': x['id'], 'title': title, 'status': 'Started' }
                save_item(new_item)
    elif request.form.get('option') == 'complete':
        title = request.form.get('title')
        for x in get_items():
            if x['title'] == title:
                new_item = { 'id': x['id'], 'title': title, 'status': 'Completed' }
                save_item(new_item)
    elif request.form.get('option') == 'delete':
        title = request.form.get('title')
        remove_item(title)
    return redirect("http://localhost:5000/")

