from flask import Blueprint, flash, render_template, session, request, flash
from .helpers import login_required
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
@login_required
def index():
    return render_template("index.html")

@main_bp.route("/login", methods=["GET", "POST"])
def login():
    # Clear current session
    session.clear()

    # Gets uername and password that was input
    if request.method == "POST":

        # Verify username was submitted
        if not request.form.get("username"):
            flash(f"Please provide a username", "danger")
            return render_template("login.html")
        
        # Verify password was submitted
        if not request.form.get("password"):
            flash(f"Please provide a password", "danger")
            return render_template("login.html")

        # Grab username and password
        username = request.form.get("username")
        password = request.form.get("password")

        # Grab user data from database
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        conn.close()

        # Verify user is in databse
        if user is None:
            flash("Invalid username and/or password", "danger")
            return render_template("login.html")
        else:
            # Verify password is correct
            if check_password_hash(user[2], password):
                session["user_id"] = user[0]
                return render_template("index.html")
            else:
                # or return invalid
                flash("Invalid username and/or password", "danger")
                return render_template("login.html")

    else:
        # If user reached route via GET (as by clicking a link or via redirect), return login form
        return render_template("login.html")
    

@main_bp.route("/logout")
def logout():
    # Clear session
    session.clear()
    # Redirect to login form
    flash("You have been logged out", "info")
    return render_template("login.html")

@main_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Verify username was submitted
        if not request.form.get("username"):
            flash(f"Please select a username", "danger")
            return render_template("register.html")
        
        # Verify password was submitted
        if not request.form.get("password"):
            flash(f"Please provide a new password", "danger")
            return render_template("register.html")

        # Grab username and password
        username = request.form.get("username")
        password = request.form.get("password")

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert new user into database
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        try:
            c.execute('INSERT INTO users (username, pwd_hash) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
        except sqlite3.IntegrityError:
            flash("Username already taken. Try another username.", "danger")
            return render_template("register.html")
        finally:
            conn.close()

        flash("Registration successful!", "success")
        session["user_id"] = c.lastrowid
        return render_template("index.html")

    else:
        return render_template("register.html")
