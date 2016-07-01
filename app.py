# -*- coding: utf-8 -*-
from functools import wraps
from flask import Flask, request, redirect, render_template, flash, url_for, g, session, render_template_string

import sqlite3


_conn = sqlite3.connect('db.sqlite3')
_conn.execute('create table if not exists comment (id integer primary key, name TEXT, comment TEXT)')
_conn.close()


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = '3187c555-d4b1-4522-972e-793ed292f9a1'


class Comment(object):
    def __init__(self, name, text):
        self.name = name
        self.comment = text


@app.route('/')
def index():
    comments = []

    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    for row in c.execute('select name, comment from comment'):
        comments.append(Comment(*row))

    conn.close()

    return render_template('index.html', comments=comments)


@app.route('/comment', methods=['POST'])
def comment():
    comment_name = request.form['name']
    comment_text = request.form['comment']

    conn = sqlite3.connect('db.sqlite3')
    with conn:
        conn.execute('insert into comment(name, comment) values (?, ?)', (comment_name, comment_text))

    conn.commit()
    conn.close()

    return redirect(url_for('index'))


@app.route('/clear-comments', methods=['GET', 'POST'])
def clear_comments():
    conn = sqlite3.connect('db.sqlite3')
    with conn:
        conn.execute('delete from comment')

    conn.commit()
    conn.close()

    return redirect(url_for('index'))


@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.args.get('q')
    return render_template('search.html', query=query)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        return redirect(url_for('index'))
    else:
        return render_template("login.html")




if __name__ == '__main__':
    app.run(host='0.0.0.0')
