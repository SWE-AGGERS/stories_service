import datetime

from flask import Flask

from stories_service.database import db, Story
from stories_service.views import blueprints
from stories_service.constants import TIMEOUT_DB




def create_app(debug=False):
    app = Flask(__name__)
    app.config['WTF_CSRF_SECRET_KEY'] = 'A SECRET KEY'
    app.config['SECRET_KEY'] = 'ANOTHER ONE'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storytellers.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # DEBUGGING AND TESTING
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['TESTING'] = debug
    app.config['LOGIN_DISABLED'] = not debug
    app.config['WTF_CSRF_ENABLED'] = debug

    for bp in blueprints:
        app.register_blueprint(bp)
        bp.app = app

    db.init_app(app)
    db.create_all(app=app)

    with app.app_context():
        q = db.session.query(Story).filter(Story.id == 1)
        story = q.first()
        if story is None:
            example = Story()
            example.text = 'Trial story of example admin user :)'
            example.likes = 42
            example.author_id = 1
            example.dicenumber = 6
            example.roll = {'dice': ['bike', 'tulip', 'happy', 'cat', 'ladder', 'rain']}
            example.date = datetime.datetime(2019, 11, 5)
            db.session.add(example)
            db.session.commit()


    return app


if __name__ == '__main__':

    app = create_app()
    app.run()