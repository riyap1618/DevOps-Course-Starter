from flask import Flask, render_template, redirect, request, url_for
from todo_app.flask_config import Config
from todo_app.data.trello_items import get_all_cards, add_card, start_card, complete_card, delete_card, redo_card, \
    change_description, change_date

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    return render_template('index.html', listOfItems=get_all_cards())


@app.route('/add', methods=['POST'])
def add():
    add_card(request.form.get('title'), request.form.get('desc'), request.form.get('date'))
    return redirect(url_for('index'))


@app.route('/start', methods=['POST'])
def start():
    start_card(request.form['startButton'])
    return redirect(url_for('index'))


@app.route('/complete', methods=['POST'])
def complete():
    complete_card(request.form['completeButton'])
    return redirect(url_for('index'))


@app.route('/redo', methods=['POST'])
def redo():
    redo_card(request.form['redoButton'])
    return redirect(url_for('index'))


@app.route('/delete', methods=['POST'])
def delete():
    delete_card(request.form['deleteButton'])
    return redirect(url_for('index'))


@app.route('/add/description', methods=['POST'])
def add_description():
    change_description(request.form['descriptionButton'], request.form.get('addDesc'))
    return redirect(url_for('index'))


@app.route('/add/date', methods=['POST'])
def add_date():
    change_date(request.form['dateButton'], request.form.get('addDate'))
    return redirect(url_for('index'))


@app.route('/remove/description', methods=['POST'])
def remove_description():
    change_description(request.form['removeDescriptionButton'], "")
    return redirect(url_for('index'))


@app.route('/remove/date', methods=['POST'])
def remove_date():
    change_date(request.form['removeDateButton'], "")
    return redirect(url_for('index'))
