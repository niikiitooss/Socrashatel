from flask import Flask, render_template, request, redirect, session
from db import *
import hashlib, random, os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder='templates', static_folder='templates/static')
app.secret_key = os.urandom(30).hex()
app.config['JWT_SECRET_KEY'] = 'super-secret'

if len(getAccesses()) == 0:
    i = 0
    accesses = [["public","публичный"],["general","общий"],["private","приватный"]]
    while i < len(accesses):
        addAccesses(accesses[i][0],accesses[i][1])
        i = i + 1

@app.route('/', methods=['post', 'get'])
def index():
    long_link = request.form.get('long_link')
    accesses = request.form.get('accesses')
    pseudonym = request.form.get('pseudonym')
    massage = ''
    if long_link != None:
        if 'user' in session:
            userLongLink = getLongUser(long_link, session['user'])
            print(getLongUser(long_link, session['user']))
            if len(userLongLink) == 0:
                if pseudonym:
                    checkPseudonym = getPseudonym(pseudonym)
                    if len(checkPseudonym) == 0:
                        addLink(long_link, pseudonym, accesses, session['user'])
                    else:
                        massage = 'Данный псевдоним занят'
                else:
                    user_short_link = hashlib.md5(long_link.encode()).hexdigest()[:random.randint(8, 12)]
                    addLink(long_link,user_short_link,accesses,session['user'])
            else:
                massage = 'Вы уже сокращали эту ссылку'
        else:
            massage = 'Войдите чтобы сокращать ссылки'
    return render_template("index.html", massage=massage)

@app.route('/auth', methods=['post', 'get'])
def auth():
    massage = ''
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        user = getUser(login)
        if login != "" and password != "":
            if len(user) > 0:
                if check_password_hash(user[0][0], password) == True:
                    auth_user = getUserId(login)[0]
                    session['user'] = auth_user
                    return redirect('/profile')
                else:
                    massage = 'Пароль неверный'
            else:
                massage = 'Такой пользователя нет'
        else:
            massage = 'Неверный логин или пароль'

    return render_template("auth.html", massage=massage)

@app.route('/reg', methods=['post', 'get'])
def reg():
    massage = ''
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        confirmPassword = request.form.get('confirm_password')
        user = getUser(login)
        print(user)
        if login != "" and password != "":
            if len(user) == 0:
                if confirmPassword == password:
                    hash_password = generate_password_hash(password)
                    registr(login, hash_password)
                else:
                    massage = 'Пароли не совпадают'
            else:
                massage = 'Такой пользователь уже зарегестрирован'
        else:
            massage = 'Неверный логин или пароль'

    return render_template("reg.html", massage=massage)

@app.route('/profile', methods=['post', 'get'])
def profile():
    long_name = request.form.get('long_name')
    edit_long_name = request.form.get('edit_long_name')
    userlinks = getUserLinks(session['user'])
    hosthref = request.host_url

    if long_name:
        deleteLink(long_name,session['user'])
        return redirect('/profile')

    if edit_long_name:
        long = request.form.get('long')
        short = request.form.get('short')
        pseudonym = request.form.get('pseudonym')
        access = request.form.get('access')
        print("ffdfd")
        if long != None and short != None:
            if pseudonym == "on":
                user_short_link = hashlib.md5(long.encode()).hexdigest()[:random.randint(8, 12)]
                updateLink(long, user_short_link, access, session['user'])
                print("1")
                return redirect('/profile')
            elif pseudonym == None and userlinks[0][2] != access:
                updateLink(long, short, access, session['user'])
                print("2")
                return redirect('/profile')
            else:
                if len(getPseudonym(short)) == 0:
                    updateLink(long, short, access, session['user'])
                    return redirect('/profile')
                else:
                    massage = 'Данный псевдоним занят'
    return render_template("/profile.html", userlinks=userlinks, hosthref=hosthref)

@app.route('/logout', methods=['post', 'get'])
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run()