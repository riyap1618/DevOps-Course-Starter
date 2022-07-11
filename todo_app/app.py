from flask import Flask, render_template, redirect, request, url_for

from todo_app.flask_config import Config
from todo_app.data.session_items import get_items, add_item, save_item, remove_item, get_item

app = Flask(__name__)
app.config.from_object(Config())

@app.route('/')
def index():
    list=get_items()
    list = sorted(list, key=lambda item: item['status'], reverse=True)
    return render_template('index.html', listOfItems=list)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    add_item(title)
    return redirect(url_for('index'))

@app.route('/complete', methods=['POST'])
def complete():
    item = get_item(request.form['completeButton'])
    item['status'] = "Completed"
    save_item(item)
    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete():
    item = get_item(request.form['deleteButton'])
    remove_item(item['title'])
    return redirect(url_for('index'))

