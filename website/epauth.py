from flask import Blueprint, Flask, render_template, redirect, url_for, request, session, flash
from .models import User, Contents, Category
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

epauth = Blueprint('epauth', __name__)

@epauth.route("/Login", methods=["GET", "POST"])
def login():
    admin = User.query.filter_by(id=1).first()
    if(request.method == "POST"):
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username = username).first()
        if(user):
            if(check_password_hash(user.password, password)):
                login_user(user, remember=True)
                return(redirect(url_for("epmain.home")))
            else:
                flash("Incorrect password.")
        else:
            flash("User does not exist.")
    return(render_template("login.html", user=current_user, admin=admin))
    

@epauth.route("/Logout")
@login_required
def logout():
    logout_user()
    return(redirect(url_for("epmain.home")))

@epauth.route("/Signup", methods=["GET", "POST"])
def signUp():
    admin = User.query.filter_by(id=1).first()
    if(request.method == "POST"):
        username = request.form.get("username")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(username=username).first()

        if(user):   
            flash("Username already in use. Please pick another username.")
        elif(len(username) < 4):
            flash("Username must be at least 4 characters")
        elif(password1 != password2):
            flash("Passwords do not match")
        elif(len(password1) < 8):
            flash("Password must be at least 8 characters")
        else:
            new_user = User(username = username, email = email, password=generate_password_hash(password1, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(User.query.filter_by(username = username).first(), remember = True)
            return(redirect(url_for("epmain.home")))
        
    return(render_template("signup.html", user=current_user, admin=admin))
