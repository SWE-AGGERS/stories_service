import datetime

from stories_service.database import Story

def restart_db_tables(db, app):
    with app.app_context():
        db.init_app(app)
        db.drop_all(app=app)
        db.create_all(app=app)


        example = Story()
        example.text = 'Trial story of example admin user :)'
        example.likes = 42
        example.author_id = 1
        example.roll = {'dice': ['bike', 'tulip', 'happy', 'cat', 'ladder', 'rain']}
        example.date = datetime.datetime(2019, 11, 5)
        db.session.add(example)
        db.session.commit()



def delete_all_db(db, app):
    with app.app_context():
        db.init_app(app)
        db.drop_all(app=app)
        db.create_all(app=app)
