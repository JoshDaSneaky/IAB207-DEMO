from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask import render_template


db= SQLAlchemy()
app = Flask(__name__)

def createApp():

    # bootstrap
    Bootstrap5(app)

    # bcrypt
    Bcrypt(app)

    # key
    app.config['SECRET_KEY'] = 'itsasecret'

    # database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///traveldb.sqlite'

    db.init_app(app)

    # upload folder
    UPLOAD_FOLDER = 'static/img'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html', error=e)


    #blueprints
    from . import views
    app.register_blueprint(views.mainbp)

    from . import destinations
    app.register_blueprint(destinations.destbp)

    from . import auth
    app.register_blueprint(auth.authbp)

    return app