from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from werkzeug.security import generate_password_hash

db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)
    app.template_folder = "../frontend/templates"
    app.static_folder = "../frontend/static"
    app.config['SECRET_KEY'] = 'awe9ipurhfadakcjvadfjhkasdfsdljfw0984520493235oiia8sdlakjsr'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    db.init_app(app)
    
    from .views import AnalyticsBP, AuthBP, UploadBP, AdminBP, ErrorBP
    from .views.main.routes import MainBP
    
    app.register_blueprint(MainBP)
    app.register_blueprint(AnalyticsBP)
    app.register_blueprint(AuthBP)
    app.register_blueprint(UploadBP)
    app.register_blueprint(AdminBP)
    app.register_blueprint(ErrorBP)
    
    from .models import User, CSV, AdminUser
    create_database(app)
    with app.app_context():
        #admin = AdminUser(email='admin@gmail.com', password=generate_password_hash('password'), firstName='Admin')
        #db.session.add(admin)
        #db.session.commit()
        pass
    login_manager = LoginManager()
    login_manager.login_view = 'pages.auth.auth.login'
    login_manager.login_message = ''
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

def create_database(app):
    with app.app_context():
        db.create_all()
        print('Created Database!')