from flask import Flask, render_template, request, redirect, jsonify
from db import *
from flask_jwt_extended import create_access_token, JWTManager, get_jwt_identity, jwt_required
import uuid, hashlib, random, os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder='templates', static_folder='templates/static')

@app.route('/', methods=['post', 'get'])
def index():

    return render_template("index.html")

@app.route('/auth', methods=['post', 'get'])
def auth():
    massage = ''
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        user = searchUser(login)
        print(user)
        if login != "" and password != "":
            if user != None:
                if check_password_hash(user[0], password) == True:
                    massage = 'Успешный вход'
                    auth_user = searchUserId(login)[0]
                    return redirect('/profile')
                else:
                    massage = 'Неверный пароль'
            else:
                massage = 'Такой пользователь не зарегистрирован '
        else:
            massage = 'Неверный логин / пароль'

    return render_template("auth.html", massage=massage)

@app.route('/reg', methods=['post', 'get'])
def reg():
    massage = ''
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        confirmPassword = request.form.get('confirm_password')
        user = searchUser(login)
        if login != "" and password != "":
            if user == None:
                if confirmPassword == password:
                    hash_password = generate_password_hash(password)
                    registration(login, hash_password)
                else:
                    massage = 'Пароли не совпадают'
            else:
                massage = 'Такой пользователь уже зарегестрирован'
        else:
            massage = 'Неверный логин / пароль'

    return render_template("reg.html", massage=massage)

@app.route('/profile', methods=['post', 'get'])
def profile():
    return render_template("/profile.html")

if __name__ == '__main__':
    app.run()