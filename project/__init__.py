from flask import Flask


def create_app():
    app = Flask(__name__)

    from project import routes

    app.register_blueprint(routes.main_blueprint)
    return app