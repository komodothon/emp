"""app/routes/auth.py"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse  import urlparse

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
    form = LoginForm()
    print("[DEBUG] login() route hit")
    
    # Check if the user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        print(f"[login] request.method = post")

        username = form.username.data
        user_cred = form.password.data
        print(f"[login]: username: {username}")

        if not username and not user_cred:
            flash("Username and password required", "warning")
            return render_template("login.html", form=form)
        
        try:
            user = User.query.filter_by(username=username).first()

            if user and user.check_password(user_cred):
                print(f"[login] user found: {user}")
                login_user(user)
                
                flash(f"Logged in as {user.username}", "success")

                next_page = request.args.get("next")
                print(f"[login]: next_page: {next_page}")

                if not next_page or urlparse(next_page).netloc != "":
                    next_page = url_for("main.dashboard")
                    print(f"[login]: next_page: {next_page}")

                print(f"[login] redirecting to {next_page}")
                print(f"[login] current_user.is_authenticated = {current_user.is_authenticated}")

                return redirect(next_page)

            else:
                flash("Invalid username or password", "danger")
                print(f"[login]: Invalid username or password")

        except Exception as e:
            print(f"[Login error]: {e}")
            flash("An error occurred. Please try again.", "danger")

    return render_template("login.html", form=form)


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