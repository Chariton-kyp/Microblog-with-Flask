from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config_forum import Config
from flask_moment import Moment

forum_db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'login.login'
moment = Moment()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    forum_db.init_app(app)
    migrate.init_app(app, forum_db)
    login.init_app(app)
    moment.init_app(app)

    
    from app.forum.main_forum import main_forum
    from app.forum.login import bp as login_bp


    app.register_blueprint(main_forum)
    app.register_blueprint(login_bp,url_prefix='/login')


    return app

from app.forum import models

    