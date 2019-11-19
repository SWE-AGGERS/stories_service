import unittest
import json
from flask import request, jsonify
from stories_service.app import create_app
from stories_service.database import db, Story
from stories_service.tests.restart_db import restart_db_tables
import sys

_app = None

class TestNewStory(unittest.TestCase):
    def test_roll(self):

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


            # wrong dice number
            reply = client.get('/rolldice/12/basic')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], -2)

            # non-existing dice set
            reply = client.get('/rolldice/6/pippo')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 404)

            # correct roll
            reply = client.get('/rolldice/5/basic')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 1)




            # logout
            reply = client.post('/logout',
                             data=json.dumps({
                                "email": "example@example.com",
                                "password": 'admin'}), content_type='application/json')

            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 1)



    def test_valid_post(self):




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




            reply = client.get('/stories')
            self.assertEqual(reply.status_code, 200)
            assert b'Trial story of example admin user' in reply.data




            # post a new story
            roll = json.dumps(["bird", "whale", "coffee", "bananas", "ladder", "glasses"])


            # RIVEDERE QUESTO

            reply = client.post('/stories', data=dict(text="bird whale coffee bananas ladder glasses", roll=roll))


            self.assertEqual(reply.status_code, 200)
            assert b'bird whale coffee bananas ladder glasses' in reply.data



            # check database entry
            q = db.session.query(Story).order_by(Story.id.desc()).first()
            self.assertEqual(q.text, "bird whale coffee bananas ladder glasses")
            self.assertEqual(q.dicenumber, 6)


            # logout
            reply = client.post('/logout',
                             data=json.dumps({
                                "email": "example@example.com",
                                "password": 'admin'}), content_type='application/json')

            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 1)




    def test_invalid_post(self):




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




            reply = client.get('/stories')
            self.assertEqual(reply.status_code, 200)
            assert b'Trial story of example admin user' in reply.data




            # post a new story
            roll = json.dumps(["bird", "whale", "coffee", "bananas", "ladder", "glasses"])


            reply = client.post('/stories', data=dict(text="Just a new story for test purposes!", roll=roll))

            self.assertEqual(reply.status_code, 200)

            #print(reply.data)

            assert b'Invalid story. Try again!' in reply.data

            # check database entry
            q = db.session.query(Story).order_by(Story.id.desc()).first()
            self.assertNotEqual(q.text, "Just a new story for test purposes!")


            # logout
            reply = client.post('/logout',
                             data=json.dumps({
                                "email": "example@example.com",
                                "password": 'admin'}), content_type='application/json')

            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 1)





    def test_invalid_post_short_story(self):




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






            reply = client.get('/stories')
            self.assertEqual(reply.status_code, 200)
            assert b'Trial story of example admin user' in reply.data




            # post a new story
            roll = json.dumps(["bird", "whale", "coffee", "bananas", "ladder", "glasses"])


            reply = client.post('/stories', data=dict(text="short story", roll=roll))

            self.assertEqual(reply.status_code, 200)

            assert b'The number of words of the story must greater or equal of the number of resulted faces.' in reply.data

            # check database entry
            q = db.session.query(Story).order_by(Story.id.desc()).first()
            self.assertNotEqual(q.text, "short story")


            # logout
            reply = client.post('/logout',
                             data=json.dumps({
                                "email": "example@example.com",
                                "password": 'admin'}), content_type='application/json')

            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 1)





    def test_invalid_post_too_long_story(self):




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





            reply = client.get('/stories')
            self.assertEqual(reply.status_code, 200)
            assert b'Trial story of example admin user' in reply.data




            # post a new story
            roll = json.dumps(["bird", "whale", "coffee", "bananas", "ladder", "glasses"])


            text = ""
            for i in range(0,2000):
                text = text + " a"

            print('ERROR 2', file=sys.stderr)

            reply = client.post('/stories', data=dict(text=text, roll=roll))

            self.assertEqual(reply.status_code, 200)

            assert b'The story is too long' in reply.data

            # check database entry
            q = db.session.query(Story).order_by(Story.id.desc()).first()
            self.assertNotEqual(q.text, text)


            # logout
            reply = client.post('/logout',
                             data=json.dumps({
                                "email": "example@example.com",
                                "password": 'admin'}), content_type='application/json')

            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 1)



if __name__ == '__main__':
    unittest.main()