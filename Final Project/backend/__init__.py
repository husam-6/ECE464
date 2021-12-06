from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail, Message

db = SQLAlchemy()
def create_app(): 
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'ladturdy@gmail.com'
    app.config['MAIL_PASSWORD'] = '@#$%^&*(P'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True 

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .archive import arch as arch_blueprint
    app.register_blueprint(arch_blueprint)

    from .grade import grade as grade_blueprint
    app.register_blueprint(grade_blueprint)

    from .notifs import notifs as notifs_blueprint 
    app.register_blueprint(notifs_blueprint)

    # from .testSend import testSend as send_blueprint
    # app.register_blueprint(send_blueprint)

    return app
