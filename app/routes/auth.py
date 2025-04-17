"""app/routes/auth.py"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from extensions import db, loginmanager, bcrypt
from app.models import User
from app.forms import LoginForm

auth_bp = Blueprint("auth", __name__)

@loginmanager.user_loader
def load_user(user_id):
    try:
        return db.session.get(User, int(user_id))
    except Exception as e:
        print(f"[User Loader Error]: {e}")
        return None

@auth_bp.route("/", methods=["GET", "POST"])
def login():        
        login_form = LoginForm()
        
        # Check if the user is already logged in
        if current_user.is_authenticated:
            return redirect(url_for("main.dashboard"))
        
        if request.method == "POST":
            username = request.form.get("username")
            user_cred = request.form.get("password")

            if not username and not user_cred:
                flash("Username and password required", "warning")
                return render_template("login.html", form=login_form)
            
            print(f"username: {username}; user_cred: {user_cred}")
            
            try:
                user = User.query.filter_by(username=username).first()
                print(f"User found: {user}")
                print(f"password on record: {user.credential.password_hash}")
                if user and user.check_password(user_cred):
                    login_user(user)
                    print("user logged in: {user.username}")

                    flash(f"Logged in as {user.username}", "success")
                    return redirect(url_for("main.dashboard"))
                else:
                    flash("Invalid username or password", "danger")

            except Exception as e:
                print(f"[Login error]: {e}")
                flash("An error occurred. Please try again.", "danger")
        return render_template("login.html", form=login_form)

@auth_bp.route("/logout")
@login_required
def logout():
    try:
        logout_user()
        flash("You have been logged out.", "info")
    except Exception as e:
        print(f"[Logout error]: {e}")
        flash("Logout failed. Please try again later.", "danger")
    return redirect(url_for("auth.login"))