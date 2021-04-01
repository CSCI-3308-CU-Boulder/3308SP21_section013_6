from flask import Flask, jsonify, render_template, request, redirect, url_for
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

basedir = os.path.abspath(os.path.dirname(__file__)) # get base directory for dropbox reference
app.config["DEBUG"] = True

# test1 = db.Table('users', db.metadata, autoload=True, autoload_with=db.engine)

# class User(db.Model):
#     __tablename__ = "users"
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(128), unique=True, nullable=False)
#     active = db.Column(db.Boolean(), default=True, nullable=False)
#     def __init__(self, email):
#         self.email = email


app.config.update( # dropbox config
    UPLOADED_PATH=os.path.join(basedir, 'static/uuids'),
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=1,
    DROPZONE_UPLOAD_MULTIPLE=0,
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    # DROPZONE_REDIRECT_VIEW=upload
    # DROPZONE_DEFAULT_MESSAGE='<p class="btn btn-dark blockyButton" />Upload an Image!</p>'
)


@app.route('/', methods = ['GET'])
def home():
    key='NGGYU' # default audio uuid
    if request.args: # if a uuid has been supplied
        key=request.args.get('uuid')
    return render_template("home.html", uuid=key)


@app.route('/upload', methods = ['POST'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        if f != None:
            # pp.makeUUID() turns image into uuid-named image and audio files
            image_id = pp.makeUUID(f, app.config['UPLOADED_PATH'])
            return redirect(url_for('home', uuid=image_id))


@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    # results = db.session.query(test1).all()
    # error = results
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

