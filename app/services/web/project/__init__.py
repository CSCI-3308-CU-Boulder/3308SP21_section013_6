from flask import Flask, jsonify, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from flask_dropzone import Dropzone
import photophonic as pp # main audio generation and image processing definitions


app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)
dropzone = Dropzone(app)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, email):
        self.email = email

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


UPLOAD_FOLDER = '/project/static/uuids/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.config['SECRET_KEY'] = 'something only you know'


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/upload/", methods=['POST'], endpoint='upload_file')
def upload():
    if request.method == 'POST':
        if request.form['button'] == 'upload':
            print("[INFO]: Request got!")

            # Checks if file is empty (page was loaded without one)
            if 'file' not in request.files:
                flash('No file part')
                return render_template("home.html")
            file = request.files['file']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                flash('No selected file')
                return render_template("home.html")
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                print('file uploaded successfully')
        else:
            print("[INFO]: DEAD BUTTON!")
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
            filename = pp.colorMark('hedgehog', '.jpeg')
            return render_template(     "result.html",
                                        image='hedgehog.jpeg',
                                        dimensions=pp.getImageDimensions('hedgehog.jpeg'),
                                        markedImage=filename
                                    )
        elif request.form['submit_button'] == 'Cloud':
            filename = pp.colorMark('cloud', '.jpg')
            return render_template(     "result.html",
                                        image='cloud.jpg',
                                        dimensions=pp.getImageDimensions('cloud.jpg'),
                                        markedImage=filename
                                   )
        else:
            pass  # unknown
    elif request.method == 'GET':
        return render_template('result.html')
