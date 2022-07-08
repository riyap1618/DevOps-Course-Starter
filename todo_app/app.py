from flask import Flask, render_template, redirect, request, url_for
from todo_app.flask_config import Config
from todo_app.data.session_items import get_items, add_item

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    return render_template('index.html', listOfItems=get_items())

@app.route('/', methods=['POST'])
def add():
    title = request.form.get('title')
    item = add_item(title)
    return redirect(url_for('index'))
