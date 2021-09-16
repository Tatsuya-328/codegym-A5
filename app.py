import os
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, register_check, login_check

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#use SQLite database
con = sqlite3.connect('spotify.db', check_same_thread=False)
db = con.cursor()

@app.route('/', methods = ['GET'])
@login_required
def index():
  return render_template('index.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        username = request.form.get("username")
        
        used_email = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchall()

        # Ensure email, password, confirmation password, username was submitted
        if register_check(email, password, confirmation, username, used_email):
            # Insert user data
            db.execute("INSERT INTO users (email, hash, username) VALUES(?, ?, ?)", (email, generate_password_hash(password), username))
            con.commit()

            users = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall()

            # Ensure username exists and password is correct
            if not check_password_hash(users[0][2], password):
                return render_template("register.html")

            session["user_id"] = users[0][1]
            # Redirect user to home page
            return redirect("/")
        else:
            return render_template("register.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        users = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchall()
        # Ensure email, password was submitted
        # Query database for username
        if login_check(email, password, users):
            # Ensure username exists and password is correct
            if not check_password_hash(users[0][2], password):
                return render_template("login.html")

            # Remember which user has logged in
            session["user_id"] = users[0][1]

            # Redirect user to home page
            return redirect("/")
        else:
            return render_template("login.html")
    # User reached route via GET (as by clicking a link or via redirect)
    else :
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")


# spotify branch test
@app.route('/', methods = ['POST'])
def spotify():
  return render_template('index.html')

if __name__ == '__main__':
  app.run(host=os.getenv('APP_ADDRESS', 'localhost'), port=5000)