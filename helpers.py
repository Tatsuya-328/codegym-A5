from flask import redirect, render_template, request, session
from functools import wraps


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def register_check(email, password, confirmation, username, used_email):
    if not email or not password or not confirmation or not username:
        return False
    elif used_email != []:
        return False
    elif password != confirmation:
        return False
    else:
        return True 

def login_check(email, password, users):
    if not email or not password:
        return False
    elif len(users) != 1:
        return False
    else:
        return True 
    