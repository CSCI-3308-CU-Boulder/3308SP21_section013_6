from flask import render_template
from app import app

IMAGES_PATH = os.path.join('static', 'images')

@app.route("/home")
def home():
    return render_template("home.html")aw


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/account_reg")
def account_reg():
    return render_template("account_reg.html")