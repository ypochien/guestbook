import shelve

import datetime
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


@application.template_filter('nl2br')
def nl2br_filter(s):
    return escape(s).replace('\n', Markup('<BR>'))


@application.template_filter('datetime_fmt')
def datetime_fmt_filter(dt):
    return dt.strftime('%Y/%m/%d %H:%M:%S')


@application.route('/')
def index():
    greeting_list = load_data()
    return render_template('index.html', greeting_list=greeting_list)


@application.route('/post', methods=['post'])
def post():
    name = request.form.get('name')
    comment = request.form.get('comment')
    create_at = datetime.datetime.now()
    save_data(name, comment, create_at)

    return redirect('/')


if __name__ == '__main__':
    application.run('127.0.0.1', 9487, debug=True)
