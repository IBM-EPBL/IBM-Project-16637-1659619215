#Imported Libraries
from flask import Flask, app, request, render_template
import os
import flask
import re
import flask_login


app = Flask(__name__)
app.secret_key = 'apple'
login_manager = flask_login.LoginManager()

login_manager.init_app(app)
users = {'a@b.c': {'password': '123'}}
class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email
    return user
@app.route('/')
def index():
    if(flask_login.current_user.is_authenticated):
        return render_template('dashboard.html')
    else:
        return render_template('login.html')
#Register function declared
@app.route('/register',methods = ['GET','POST'])
def register():
    error = None
    if(flask.request.method == 'GET'):
        return render_template('register.html')
    email = flask.request.form['email']
    if(email in users):
        return render_template('register.html',flash_message='True')
    else:
        users[email]={'password':flask.request.form['password']}
        user  = User()
        user.id = email
        flask_login.login_user(user)
        return render_template('dashboard.html',flash_message='True')


#Login function declared
@app.route('/login',methods =['GET','POST'])
def login():
    error = None
    if(flask.request.method == 'GET'):
        
        return render_template('login.html',flash_message='False')
    email = flask.request.form['email']
    if(email in users and flask.request.form['password']==users[email]['password']):
        user  = User()
        user.id = email
        flask_login.login_user(user)
        return render_template('dashboard.html',flash_message='Fal')
    #flask.flash('invalid credentials !!!')
    return render_template('login.html',flash_message="True")
    #error = 'inavlid credentials')

#Dashboard function declared
@app.route('/dashboard',methods = ['GET','POST'])
@flask_login.login_required
def dashboard():
    if(flask.request.method == 'GET'):
        return render_template('dashboard.html',flash_message='False')
    email = flask.request.form['email']
    if(email in users and flask.request.form['password']==users[email]['password']):
        user  = User()
        user.id = email
        flask_login.login_user(user)
        return render_template('dashboard.html',flash_message="Fal")
    return render_template('dashboard.html',flash_message="Fals")

#Logout function declared
@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return render_template('logout.html')


@app.route('/prediction')
@flask_login.login_required
def prediction():
    return render_template('prediction.html')


if __name__ == '__main__':
    app.run(debug=True,port = 8000)
