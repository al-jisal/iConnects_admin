from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config


db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # initiates the database
    db.init_app(app)
    migrate.init_app(app, db)

    # creates the tables
    with app.app_context():
        from project.models import Student, Alum, Post
        from project.data import students_data, alumni_data, posts_data
        db.create_all()

        # loads the data into the database
        db.session.bulk_insert_mappings(Student, students_data)
        db.session.bulk_insert_mappings(Alum, alumni_data)
        db.session.bulk_insert_mappings(Post, posts_data)
        db.session.commit()

    # registers the blueprint
    from project import routes
    app.register_blueprint(routes.main_blueprint)

    return app