from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app, db, bcrypt
from application.auth.models import User
from application.auth.forms import LoginForm, RegisterationForm

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)

    if not form.validate():
        return render_template("auth/loginform.html",
                               form = form)

    user = User.query.filter_by(username=form.username.data).first()
    if not user:
        return render_template("auth/loginform.html", form = form,
                               error = "No such username or password")

    
    if not user.check_password(form.password.data):
        return render_template("auth/loginform.html", form = form,
                               error = "No such username or password")


    login_user(user)
    return redirect(url_for("hello"))

@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("hello"))

@app.route("/auth/register", methods = ["GET", "POST"])
def auth_register():
    if request.method == "GET":
        return render_template("auth/registerationform.html",
                               form = RegisterationForm())
    form = RegisterationForm(request.form)

    if form.password.data != form.repeat.data:
        error = "Passwords and repeat didn't match"
        return render_template("auth/registerationform.html", error = error,
                               form = form)

    if not form.validate():
        return render_template("auth/registerationform.html",
                               form = form)

    u = User(form.name.data, form.username.data,
             bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))

    if does_exist_name(u):
        error = "name is laready taken"
        return render_template("auth/registerationform.html", error = error,
                               form = form)

    if does_exist_username(u):
        error = "username is laready taken"
        return render_template("auth/registerationform.html", error = error,
                               form = form)


    db.session().add(u)
    db.session().commit()
    login_user(u)

    return redirect(url_for("hello"))

def does_exist_name(user):
    name = User.query.filter_by(name=user.name).first()

    if name:
        return True

    return False

def does_exist_username(user):
    username = User.query.filter_by(username=user.username).first()

    if username:
        return True

    return False
