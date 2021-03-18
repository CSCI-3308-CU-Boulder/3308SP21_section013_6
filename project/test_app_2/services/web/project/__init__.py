from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import photophonic as pp # main audio generation and image processing definitions


app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, email):
        self.email = email


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/account_reg")
def account_reg():
    return render_template("account_reg.html")


@app.route("/creations")
def creations():
    return render_template("creations.html")


@app.route('/test',methods = ['POST', 'GET'])
def test():
    return render_template("test.html")


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Hedgehog':
            return render_template( "result.html", result='hedgehog.jpeg', dimensions=pp.getImageDimensions('hedgehog.jpeg') )
        elif request.form['submit_button'] == 'Cloud':
            return render_template("result.html", result='cloud.jpg', dimensions=pp.getImageDimensions('cloud.jpg') )
        else:
            pass  # unknown
    elif request.method == 'GET':
        return render_template('result.html')
