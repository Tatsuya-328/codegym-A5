import os
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required

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
        
        # print(username)
        users = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchall()

        # Ensure email was submitted
        if not email:
            return render_template("register.html")

        elif users != []:
            # print(len(username))
            # print(users)
            return render_template("register.html")

        # Ensure password was submitted
        elif not password:
            return render_template("register.html")

        # Ensure confirmation password was submitted
        elif not confirmation:
            return render_template("register.html")

        if password == confirmation:
            db.execute("INSERT INTO users (email, hash, username) VALUES(?, ?, ?)", (email, generate_password_hash(password), username))
            con.commit()

            rows = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall()

            # Ensure username exists and password is correct
            # print(rows)
            
            if  not check_password_hash(rows[0][2], password):
                flash("invalid username and/or password")
                return render_template("register.html")

            session["user_id"] = rows[0][1]
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
        # Ensure username was submitted
        if not email:
            return render_template("login.html")

        # Ensure password was submitted
        elif not password:
            return render_template("login.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchall()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0][2], password):
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0][1]

        # Redirect user to home page
        return redirect("/")

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
  app.run(host=os.getenv('APP_ADDRESS', 'localhost'), port=8200)
  # app()