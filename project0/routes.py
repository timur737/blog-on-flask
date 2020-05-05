from flask import render_template, redirect, flash, url_for, request
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from project0 import app, db
from project0.models import Message, User


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', messages=Message.query.all())


@app.route('/main', methods=['GET'])
@login_required
def main():
    return render_template('twit.html')


@app.route('/add_message', methods=['POST'])
def add_message():
    text = request.form.get('text')
    tag = request.form.get('tag')
    db.session.add(Message(text, tag))
    db.session.commit()
    return redirect(url_for('main'))


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')
    if login and password:
        user = User.query.filter_by(login=login).first()

        if user and check_password_hash(user.password, password):
            login_user(user)


            # next_page = request.args.get('next')

            return redirect(url_for('main'))

        else:
            flash('Login or password is not correct')
    else:
        flash('Please fill login and password fields')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    if request.method == 'POST':
        if not (login or password or password2):
            flash('Please fill all fields!')
        elif password != password2:
            flash('Passwords are not equal')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login_page'))
    return render_template('reg.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)
    return response
