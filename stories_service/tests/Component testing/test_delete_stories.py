import unittest
from stories_service.app import create_app
from stories_service.database import db, Story
from flask_login import current_user
from flask import json, jsonify
from stories_service.restart_db import restart_db_tables

_app = None


class TestDeleteStory(unittest.TestCase):

    def test_delete_story_positive(self):

        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            # login
            reply = client.post('/login',
                             data=json.dumps({
                                "email": "example@example.com",
                                "password": 'admin'}), content_type='application/json')

            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['response'], True)
            self.assertEqual(body['user_id'], 1)





            reply = client.get('/allusers')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 1)

            # add reaction to a story
            reply = client.get('/stories/reaction/1/1')
            self.assertEqual(reply.status_code, 200)

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertNotEqual(story, None)

            stories = Story.query.filter_by(id=1).all()
            self.assertEqual(len(stories), 1)

            # Request of total number of reactions of story 1

            reply = client.get('/reactions/1')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 1)

            # Request of total number of users

            reply = client.get('/allusers')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 1)



            reply = client.post('/stories/remove/1')
            self.assertEqual(reply.status_code, 200)
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 1)


            reply = client.get('/reactions/1')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 0)

            # logout
            reply = client.post('/logout',
                             data=json.dumps({
                                "email": "example@example.com",
                                "password": 'admin'}), content_type='application/json')

            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['response'], True)
            self.assertEqual(body['user_id'], 1)



    def test_delete_story_negative(self):

        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            # login
            reply = client.post('/login',
                             data=json.dumps({
                                "email": "example@example.com",
                                "password": 'admin'}), content_type='application/json')

            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 1)

            reply = client.get('/allusers')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 1)

            # add reaction to a story
            reply = client.get('/stories/reaction/1/1')
            self.assertEqual(reply.status_code, 200)

            reply = client.post('/stories/remove/2')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], -3)

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertNotEqual(story, None)

            reply = client.get('/reactions/1')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 1)

            stories = Story.query.filter_by(id=1).all()
            self.assertEqual(len(stories), 1)

            reply = client.get('/allusers')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 1)

            reply = client.post('/stories/remove/1')
            self.assertEqual(reply.status_code, 200)
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 1)


            reply = client.get('/reactions/1')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 0)

            # logout
            reply = client.post('/logout',
                             data=json.dumps({
                                "email": "example@example.com",
                                "password": 'admin'}), content_type='application/json')

            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 1)


    def test_delete_story_multiple_users_reactions(self):

        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            # login
            reply = client.post('/login',
                             data=json.dumps({
                                "email": "example@example.com",
                                "password": 'admin'}), content_type='application/json')

            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 1)

            # add reaction to a story
            reply = client.get('/stories/reaction/1/1')
            self.assertEqual(reply.status_code, 200)

            reply = client.get('/allusers')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 1)

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertNotEqual(story, None)

            # logout
            reply = client.post('/logout',
                             data=json.dumps({
                                "email": "example@example.com",
                                "password": 'admin'}), content_type='application/json')

            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['response'], True)
            self.assertEqual(body['user_id'], 1)


            # signup

            reply = client.post('/signup',
                             data=json.dumps({
                                "firstname": "Mario",
                                "lastname": "Rossi",
                                "email": "mario.rossi@gmail.com",
                                "dateofbirth": "1994",
                                "password": '12345'}), content_type='application/json')

            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 1)



            reply = client.get('/allusers')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 1)

            stories = Story.query.filter_by(id=1).all()
            self.assertEqual(len(stories), 1)

            reply = client.get('/reactions/1')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 0)

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertNotEqual(story, None)

            reply = client.get('/reactions/1')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 0)

            # add reaction to a story
            reply = client.get('/stories/reaction/1/1')
            self.assertEqual(reply.status_code, 200)

            # logout
            reply = client.post('/logout',
                             data=json.dumps({
                                "email": "mario.rossi@gmail.com",
                                "password": '12345'}), content_type='application/json')

            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 1)

            # login
            reply = client.post('/login',
                             data=json.dumps({
                                "email": "example@example.com",
                                "password": 'admin'}), content_type='application/json')

            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 1)

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertNotEqual(story, None)

            reply = client.get('/reactions/1')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 2)

            reply = client.post('/stories/remove/1')
            self.assertEqual(reply.status_code, 200)
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 1)


            story = db.session.query(Story).filter_by(id=1).first()
            self.assertEqual(story, None)


            # logout
            reply = client.post('/logout',
                             data=json.dumps({
                                "email": "example@example.com",
                                "password": 'admin'}), content_type='application/json')

            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 1)

    def test_delete_wrong_author_story(self):

        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            # login
            reply = client.post('/login',
                             data=json.dumps({
                                "email": "example@example.com",
                                "password": 'admin'}), content_type='application/json')

            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 1)

            # add reaction to a story
            reply = client.get('/stories/reaction/1/1')
            self.assertEqual(reply.status_code, 200)

            reply = client.get('/allusers')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 1)

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertNotEqual(story, None)

            # logout
            reply = client.post('/logout',
                             data=json.dumps({
                                "email": "example@example.com",
                                "password": 'admin'}), content_type='application/json')

            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 1)

            # signup

            reply = client.post('/signup',
                             data=json.dumps({
                                "firstname": "Mario",
                                "lastname": "Rossi",
                                "email": "mario.rossi@gmail.com",
                                "dateofbirth": "1994",
                                "password": '12345'}), content_type='application/json')
            self.assertEqual(reply.status_code, 200)
            body = json.loads(str(reply.data, 'utf8'))

            self.assertEqual(body['result'], 1)

            reply = client.get('/allusers')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 2)


            story = db.session.query(Story).filter_by(id=1).first()
            self.assertNotEqual(story, None)

            stories = Story.query.filter_by(id=1).all()
            self.assertEqual(len(stories), 1)

            reply = client.get('/reactions/1')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 1)

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertNotEqual(story, None)

            reply = client.get('/reactions/1')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 1)

            # add reaction to a story
            reply = client.get('/stories/reaction/1/1')
            self.assertEqual(reply.status_code, 200)

            reply = client.post('/stories/remove/1')
            self.assertEqual(reply.status_code, 200)
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], -2)

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertNotEqual(story, None)

            # logout
            reply = client.post('/logout',
                             data=json.dumps({
                                "email": "mario.rossi@gmail.com",
                                "password": '12345'}), content_type='application/json')

            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 1)

    def test_delete_story_positive_index(self):

        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            # login
            reply = client.post('/login',
                             data=json.dumps({
                                "email": "example@example.com",
                                "password": 'admin'}), content_type='application/json')

            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 1)

            reply = client.get('/allusers')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 1)

            # add reaction to a story
            reply = client.get('/stories/reaction/1/1')
            self.assertEqual(reply.status_code, 200)

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertNotEqual(story, None)

            stories = Story.query.filter_by(id=1).all()
            self.assertEqual(len(stories), 1)

            reply = client.get('/reactions/1')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 1)

            reply = client.get('/allusers')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 1)


            reply = client.post('/stories/remove/1')
            self.assertEqual(reply.status_code, 200)
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 1)

            reply = client.get('/reactions/1')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 1)

            # logout
            reply = client.post('/logout',
                             data=json.dumps({
                                "email": "example@example.com",
                                "password": 'admin'}), content_type='application/json')

            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 1)

    def test_delete_story_negative_index(self):

        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            # login
            reply = client.post('/login',
                             data=json.dumps({
                                "email": "example@example.com",
                                "password": 'admin'}), content_type='application/json')

            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 1)

            reply = client.get('/allusers')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 1)


            # add reaction to a story
            reply = client.get('/stories/reaction/1/1')
            self.assertEqual(reply.status_code, 200)

            reply = client.post('/stories/remove/2')
            self.assertEqual(reply.status_code, 404)

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertNotEqual(story, None)

            reply = client.get('/reactions/1')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 1)

            stories = Story.query.filter_by(id=1).all()
            self.assertEqual(len(stories), 1)

            reply = client.get('/allusers')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 1)

            reply = client.post('/stories/remove/1')
            self.assertEqual(reply.status_code, 200)
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 1)

            reply = client.get('/reactions/1')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 0)

            # logout
            reply = client.post('/logout',
                             data=json.dumps({
                                "email": "example@example.com",
                                "password": 'admin'}), content_type='application/json')

            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 1)

    def test_delete_story_multiple_users_reactions_index(self):

        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            # login
            reply = client.post('/login',
                             data=json.dumps({
                                "email": "example@example.com",
                                "password": 'admin'}), content_type='application/json')

            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 1)

            # add reaction to a story
            reply = client.get('/stories/reaction/1/1')
            self.assertEqual(reply.status_code, 200)

            reply = client.get('/allusers')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 1)

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertNotEqual(story, None)

            # logout
            reply = client.post('/logout',
                             data=json.dumps({
                                "email": "example@example.com",
                                "password": 'admin'}), content_type='application/json')

            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 1)

            # signup

            reply = client.post('/signup',
                             data=json.dumps({
                                "firstname": "Mario",
                                "lastname": "Rossi",
                                "email": "mario.rossi@gmail.com",
                                "dateofbirth": "1994",
                                "password": '12345'}), content_type='application/json')
            self.assertEqual(reply.status_code, 200)
            body = json.loads(str(reply.data, 'utf8'))

            reply = client.get('/allusers')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 2)

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertNotEqual(story, None)

            stories = Story.query.filter_by(id=1).all()
            self.assertEqual(len(stories), 1)

            reply = client.get('/reactions/1')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 1)

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertNotEqual(story, None)

            reply = client.get('/reactions/1')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 1)

            # add reaction to a story
            reply = client.get('/stories/reaction/1/1')
            self.assertEqual(reply.status_code, 200)

            # logout
            reply = client.post('/logout',
                             data=json.dumps({
                                "email": "mario.rossi@gmail.com",
                                "password": '12345'}), content_type='application/json')

            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 1)

            # login
            reply = client.post('/login',
                             data=json.dumps({
                                "email": "example@example.com",
                                "password": 'admin'}), content_type='application/json')

            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 1)

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertNotEqual(story, None)

            reply = client.get('/reactions/1')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 2)

            reply = client.post('/stories/remove/1')
            self.assertEqual(reply.status_code, 200)
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 1)

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertEqual(story, None)

            # logout
            reply = client.post('/logout',
                             data=json.dumps({
                                "email": "example@example.com",
                                "password": 'admin'}), content_type='application/json')

            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 1)



    def test_delete_wrong_author_story_index(self):

        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            # login
            reply = client.post('/login',
                             data=json.dumps({
                                "email": "example@example.com",
                                "password": 'admin'}), content_type='application/json')

            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 1)

            # add reaction to a story
            reply = client.get('/stories/reaction/1/1')
            self.assertEqual(reply.status_code, 200)

            reply = client.get('/allusers')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 1)

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertNotEqual(story, None)

            # logout
            reply = client.post('/logout',
                             data=json.dumps({
                                "email": "example@example.com",
                                "password": 'admin'}), content_type='application/json')

            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 1)

            # signup

            reply = client.post('/signup',
                             data=json.dumps({
                                "firstname": "Mario",
                                "lastname": "Rossi",
                                "email": "mario.rossi@gmail.com",
                                "dateofbirth": "1994",
                                "password": '12345'}), content_type='application/json')
            self.assertEqual(reply.status_code, 200)
            body = json.loads(str(reply.data, 'utf8'))

            reply = client.get('/allusers')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 2)

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertNotEqual(story, None)

            stories = Story.query.filter_by(id=1).all()
            self.assertEqual(len(stories), 1)

            reply = client.get('/reactions/1')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 1)

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertNotEqual(story, None)

            reply = client.get('/reactions/1')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 1)

            # add reaction to a story
            reply = client.get('/stories/reaction/1/1')
            self.assertEqual(reply.status_code, 200)

            reply = client.post('/stories/remove/1')
            self.assertEqual(reply.status_code, 200)
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 1)

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertNotEqual(story, None)

            # logout
            reply = client.post('/logout',
                             data=json.dumps({
                                "email": "mario.rossi@gmail.com",
                                "password": '12345'}), content_type='application/json')

            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 1)


if __name__ == '__main__':
    unittest.main()


