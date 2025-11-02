from flask import Flask
import secrets

def create_app():
    app = Flask(__name__)
    ## CHANGE THIS BEFORE PRODUCTION ##
    app.config['SECRET_KEY'] = secrets.token_hex(16)


    from .routes import main_bp
    from .api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
