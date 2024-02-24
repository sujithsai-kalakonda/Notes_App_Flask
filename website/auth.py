from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db  ##means from __init__.py import db
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
            else:
                flash("Incorrect password, try again!", category="error")
        else:
            flash("Email does not exist", category="error")

    return render_template("login.html", boolean=True)


@auth.route("/logout")
def logout():
    return "<p>Logout</p>"


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        firstName = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists", category="error")
        elif len(email) < 4:
            flash("Email must be greater than 3 characters", category="error")
        elif len(firstName) < 2:
            flash("First Name must be greater than 1 character", category="error")
        elif len(password2) < 7:
            flash("Password must be greater than 6 characters", category="error")
        elif password1 != password2:
            flash("Password doesn't match", category="error")

        else:
            new_user = User(
                email=email,
                first_name=firstName,
                password=generate_password_hash(password1),
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Successfully account created", category="success")
            return redirect(url_for("views.home"))

    return render_template("sign_up.html")
