from flask import app, render_template, redirect, url_for, request, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from .models import Users, db
from . import db
from flask import Blueprint, current_app, jsonify


bp = Blueprint('routes', __name__)

@bp.route("/")
def home():
    return render_template("index.html")

@bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = Users.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            flash("You have been logged in", "info")
            return redirect(url_for("routes.user", usr=user.name))
        else:
            flash("Login failed. Check your email and/or password", "danger")
            return redirect(url_for("routes.login"))
    else:
        return render_template("login.html")

@bp.route('/add', methods=["POST", "GET"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form['password1']

        if password != confirm_password:
            flash("Passwords do not match", "danger")
            return render_template('add.html')

        if len(password) < 8:
            flash("Password must be at least 8 characters long", "danger")
            return render_template("add.html")

        new_user = Users(name, email, password=generate_password_hash(password, method='pbkdf2:sha256'))
        try:
            db.session.add(new_user)
            db.session.commit()
            flash("User added successfully!", "success")
            return redirect(url_for("routes.home"))

        except IntegrityError:
            flash("Email already exists. Please use a different email.", "danger")
            return redirect(url_for("routes.add"))

        except Exception as e:
            flash(f"Error: {e}", "danger")
            return redirect(url_for("routes.add"))
    else:
        return render_template("add.html")

@bp.route("/user/<usr>")
def user(usr):
    return f"<h1>Welcome {usr}</h1>"

@bp.route('/users', methods=['GET'])
def get_users():
    users = Users.query.all()
    return jsonify([user.to_dict() for user in users])


def init_app(app):
    app.register_blueprint(bp)