from flask import Flask
from flask_cors import CORS
from datetime import timedelta
from .helper.user.user_routes import user_routes
from .helper.events.event_routes import event_routes
from .helper.votes.vote_routes import vote_routes
from .helper.availability.user_availability_routes import user_availability_routes
from .helper.sugggestions.suggestion_routes import suggestion_routes
from flask_login import LoginManager
def create_app():
    
    app = Flask(__name__)
    CORS(app)

    app.config.from_mapping(
        SECRET_KEY='your_secret_key',
        PERMANENT_SESSION_LIFETIME = timedelta(days=30),
        DATABASE='database.db',
    )
    login_manager = LoginManager(app)
    login_manager.login_view = 'login'

    from . import db
    db.init_app(app)
    app.register_blueprint(user_routes)
    app.register_blueprint(event_routes)
    app.register_blueprint(suggestion_routes)
    app.register_blueprint(vote_routes)
    app.register_blueprint(user_availability_routes)
    
    return app
