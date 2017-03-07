import shelve

from flask import Flask, request, render_template, redirect, escape, Markup

application = Flask(__name__)

DATA_FILE = 'guestbook.dat'


def save_data(name, comment, create_at):
    """
    Save Guest Comment
    :param name: Name 
    :param comment: Comment
    :param create_at: Create time
    :return: None
    """
    database = shelve.open(DATA_FILE)

    if 'greeting_list' not in database:
        getting_list = []
    else:
        getting_list = database['greeting_list']

    getting_list.insert(0, {
        'name': name,
        'comment': comment,
        'create_at': create_at
    })

    database['greeting_list'] = getting_list
    database.close()


def load_data():
    """
    
    :return: json string in list. 
    """
    database = shelve.open(DATA_FILE)
    greeting_list = database.get('greeting_list', [])
    database.close()
    return greeting_list


@application.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    application.run('127.0.0.1', 0x9487, debug=True)
