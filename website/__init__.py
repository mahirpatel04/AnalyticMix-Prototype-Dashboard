from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'awe9ipurhfadakcjvadfjhkasdfsdljfw0984520493235oiia8sdlakjsr'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    from .pages.analytics.analytics import analytics
    from .pages.upload.upload import upload
    from .pages.auth.auth import auth
    
    app.register_blueprint(analytics, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import User, CSV
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'pages.auth.login'
    login_manager.login_message = ''
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Created Database!')