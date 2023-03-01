from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "yo mama"

    from .login import login
    from .signup import signup
    from .userProfile import userProfile

    app.register_blueprint(login, url_prefix="/")
    app.register_blueprint(signup, url_prefix="/")
    app.register_blueprint(userProfile, url_prefix="/")

    return app