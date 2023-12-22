import importlib.util
import os
from flask import Flask
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_gravatar import Gravatar
from dotenv import load_dotenv
import os
# load environmental variables
load_dotenv()

# FILE_PATH_CWD = os.getenv("FILE_PATH_CWD")
# # importing the directory module as a directory and changing file path
# spec = importlib.util.spec_from_file_location(
#     "directory", FILE_PATH_CWD)
# directory = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(directory)
# path = directory.FilePath()
# path.change_working_directory(__file__)

# App Initialization
SECRET_KEY = os.getenv('SECRET_KEY')
ROOT = os.getenv('ROOT')
PATH = os.getenv('PATH')
DB_NAME = os.getenv('DB_URI_ONE')
DB_Blogs = os.getenv('DB_URI')
db = SQLAlchemy()
ckeditor = CKEditor()
FLASK_WTF_SECRET = os.getenv('WTF_CSRF_SECRET_KEY')
login_manager = LoginManager()
# contact info
MY_EMAIL = os.getenv('MY_EMAIL')
MY_PASSWORD = os.getenv('MY_PASSWORD')


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI_ONE", "sqlite:///users.db")
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "sqlite:///posts.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_Blogs",f'sqlite:///posts.db')
    app.config['PDF_SECRETS_FILE'] = ROOT
    db.init_app(app)
    # initialize bootstrap
    Bootstrap5(app)
    # initialize CKEditor
    ckeditor.init_app(app)
    # initialize login authentication
    login_manager.login_view = 'login'
    login_manager.init_app(app)
    # initialize gravatar profile images
    gravatar = Gravatar(app,
                        size=100,
                        rating='g',
                        default='retro',
                        force_default=False,
                        force_lower=False,
                        use_ssl=False,
                        base_url=None)
    from .models import User, BlogPost
    from .forms import CreatePostForm, RegistrationForm


    with app.app_context():
        db.create_all()


    # authenticating login / user_loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app, db, User, BlogPost, gravatar
    # return app, db, User, login_manager, BlogPost
