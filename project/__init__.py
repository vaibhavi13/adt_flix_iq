from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# init SQLAlchemy so we can use it later in our models

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_message = 'Please login to continue'
login_manager.login_view = 'user.login'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'root'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Jonsnow1310*@localhost:5432/ADT'
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.session_protection = "strong"

    from project.models.User import User
    from project.main.routes import main


    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from project.routes import routes as routes_blueprint
    app.register_blueprint(routes_blueprint)
    from project.models.User import User
    # blueprint for non-auth parts of app
    app.register_blueprint(main)
        
    from project.netflix.netflixUtility import netflixUtility as netflixUtility_blueprint
    app.register_blueprint(netflixUtility_blueprint)


    #from project import db, create_app, models
    with app.app_context():
        db.create_all()
        db.session.commit()

    return app