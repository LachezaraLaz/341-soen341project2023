from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "yo mama"
    UPLOAD_FOLDER = '../uploads'

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    from .login import login
    from .signup import signup
    from .userProfile import userProfile
    from .notification import notification
    from .adminPages import adminPages
    from .employerDashboard import employerDashboard
    from .home import home
    from .feedback import feedback

    app.register_blueprint(login, url_prefix="/")
    app.register_blueprint(signup, url_prefix="/")
    app.register_blueprint(userProfile, url_prefix="/")
    app.register_blueprint(notification, url_prefix="/")
    app.register_blueprint(adminPages, url_prefix=("/"))
    app.register_blueprint(employerDashboard, url_prefix=("/"))
    app.register_blueprint(home, url_prefix=("/"))
    app.register_blueprint(feedback, url_prefix=("/"))


    return app