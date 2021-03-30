from flask import Flask, jsonify, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from flask_dropzone import Dropzone
import photophonic as pp # main audio generation and image processing definitions


app = Flask(__name__)
app.config.from_object("project.config.Config")
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://hello_flask:hello_flask@db:5432/hello_flask_dev"
db = SQLAlchemy(app)
dropzone = Dropzone(app)

# test1 = db.Table('users', db.metadata, autoload=True, autoload_with=db.engine)

# class User(db.Model):
#     __tablename__ = "users"

#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(128), unique=True, nullable=False)
#     active = db.Column(db.Boolean(), default=True, nullable=False)

#     def __init__(self, email):
#         self.email = email


basedir = os.path.abspath(os.path.dirname(__file__)) # get base directory for dropbox reference

app.config.update( # dropbox config
    UPLOADED_PATH=os.path.join(basedir, 'static/uuids'),
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=1,
    DROPZONE_UPLOAD_MULTIPLE=0,
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg']),
    DROPZONE_REDIRECT_VIEW='home',
    DROPZONE_DEFAULT_MESSAGE='<button type="file" href="#" class="btn btn-dark blockyButton" />Upload an Image!</button>'
)


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':

        f = request.files.get('file')

        if f != None:
            print("[INFO]: Filename: ", f)
            file_path = os.path.join(app.config['UPLOADED_PATH'], f.filename)
            print("[INFO]: Path: ", file_path)
            f.save(file_path)
            image_id = pp.toUUID(file_path) # converts the file to a UUID name, then returns that ID
            os.remove(file_path) # delete the uploaded file (it's been renamed to a uuid)

            print("[INFO]: Image UUID is: " + image_id) # IMAGE IS NOW LOADED ON SERVER

            # ADD IMAGE ID (UUID), IMAGE DATA, AND USER SIGNATURE TO DB HERE

        else:
            print("[INFO]: NULL BUTTON")

    return render_template("home.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    # results = db.session.query(test1).all()
    error = results
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect("/")
    return render_template("login.html", error=error)


@app.route("/account_reg", methods = ['GET'])
def account_reg():
    return render_template("account_reg.html")
def user_records():
    newUsername = request.args.get('username')
    newEmail = request.args.get('email')
    newPassword = request.args.get('pwd')
    if(newUsername and newEmail and newPassword):
        # Add three items to users DB... somehow lol...
        print(newUsername)


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
