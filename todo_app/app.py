from flask import Flask
from flask import render_template
from flask import redirect, request

from todo_app.flask_config import Config
from todo_app.data.session_items import get_items
from todo_app.data.session_items import add_item

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    print(get_items())
    return render_template('index.html', listOfItems=get_items())
    #return 'Hello World!'

@app.route('/', methods=['POST'])
def add():
    title = request.form.get('title')
    item = add_item(title)
    return redirect("http://localhost:5000/")
