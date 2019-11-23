import unittest
import json
from stories_service.app import create_app
from stories_service.database import db, Story
from stories_service.restart_db import restart_db_tables
import sys

_app = None

class TestNewStory(unittest.TestCase):




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

            self.assertEqual(reply.status_code, 200)
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['response'], True)
            self.assertEqual(body['user_id'], 1)




            reply = client.get('/stories')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 1)
            self.assertEqual(len(body['stories']), 1)
            firstStory = body['stories'][0]
            self.assertEqual(firstStory['id'], 1)
            self.assertEqual(firstStory['text'], 'Trial story of example admin user :)')
            self.assertEqual(firstStory['dicenumber'], None)
            self.assertEqual(firstStory['like'], 42)
            self.assertEqual(firstStory['dislike'], None)
            self.assertEqual(firstStory['author_id'], 1)




            # post a new story
            roll = json.dumps(["bird", "whale", "coffee", "bananas", "ladder", "glasses"])


            reply = client.post('/stories?userid=1', data=dict(text="bird whale coffee bananas ladder glasses", roll=roll))


            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 1)
            self.assertEqual(body['message'], "Story created")
            self.assertEqual(len(body['stories']), 2)
            firstStory = body['stories'][0]
            self.assertEqual(firstStory['id'], 1)
            self.assertEqual(firstStory['text'], 'Trial story of example admin user :)')
            self.assertEqual(firstStory['dicenumber'], None)
            self.assertEqual(firstStory['like'], 42)
            self.assertEqual(firstStory['dislike'], None)
            self.assertEqual(firstStory['author_id'], 1)
            secondStory = body['stories'][1]
            self.assertEqual(secondStory['id'], 2)
            self.assertEqual(secondStory['text'], 'bird whale coffee bananas ladder glasses')
            #self.assertEqual(firstStory['dicenumber'], None)
            #self.assertEqual(firstStory['like'], 42)
            #self.assertEqual(firstStory['dislike'], None)
            self.assertEqual(secondStory['author_id'], 1)




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
            self.assertEqual(body['response'], True)
            self.assertEqual(body['user_id'], 1)





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

            self.assertEqual(reply.status_code, 200)
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['response'], True)
            self.assertEqual(body['user_id'], 1)




            reply = client.get('/stories')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 1)
            self.assertEqual(len(body['stories']), 1)
            firstStory = body['stories'][0]
            self.assertEqual(firstStory['id'], 1)
            self.assertEqual(firstStory['text'], 'Trial story of example admin user :)')
            self.assertEqual(firstStory['dicenumber'], None)
            self.assertEqual(firstStory['like'], 42)
            self.assertEqual(firstStory['dislike'], None)
            self.assertEqual(firstStory['author_id'], 1)




            # post a new story
            roll = json.dumps(["bird", "whale", "coffee", "bananas", "ladder", "glasses"])



            reply = client.post('/stories?userid=1', data=dict(text="bird whale coffee bananas ladder glasses", roll=roll))


            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], -6)
            self.assertEqual(body['message'], "Invalid story. Try again!")
            self.assertEqual(len(body['stories']), 1)
            firstStory = body['stories'][0]
            self.assertEqual(firstStory['id'], 1)
            self.assertEqual(firstStory['text'], 'Trial story of example admin user :)')
            self.assertEqual(firstStory['dicenumber'], None)
            self.assertEqual(firstStory['like'], 42)
            self.assertEqual(firstStory['dislike'], None)
            self.assertEqual(firstStory['author_id'], 1)




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
            self.assertEqual(body['response'], True)
            self.assertEqual(body['user_id'], 1)





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

            self.assertEqual(reply.status_code, 200)
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['response'], True)
            self.assertEqual(body['user_id'], 1)




            reply = client.get('/stories')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 1)
            self.assertEqual(len(body['stories']), 1)
            firstStory = body['stories'][0]
            self.assertEqual(firstStory['id'], 1)
            self.assertEqual(firstStory['text'], 'Trial story of example admin user :)')
            self.assertEqual(firstStory['dicenumber'], None)
            self.assertEqual(firstStory['like'], 42)
            self.assertEqual(firstStory['dislike'], None)
            self.assertEqual(firstStory['author_id'], 1)




            # post a new story
            roll = json.dumps(["bird", "whale", "coffee", "bananas", "ladder", "glasses"])



            reply = client.post('/stories?userid=1', data=dict(text="short story", roll=roll))


            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], -5)
            self.assertEqual(body['message'], "The number of words of the story must greater or equal of the number of resulted faces.")
            self.assertEqual(len(body['stories']), 1)
            firstStory = body['stories'][0]
            self.assertEqual(firstStory['id'], 1)
            self.assertEqual(firstStory['text'], 'Trial story of example admin user :)')
            self.assertEqual(firstStory['dicenumber'], None)
            self.assertEqual(firstStory['like'], 42)
            self.assertEqual(firstStory['dislike'], None)
            self.assertEqual(firstStory['author_id'], 1)




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
            self.assertEqual(body['response'], True)
            self.assertEqual(body['user_id'], 1)




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

            self.assertEqual(reply.status_code, 200)
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['response'], True)
            self.assertEqual(body['user_id'], 1)




            reply = client.get('/stories')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 1)
            self.assertEqual(len(body['stories']), 1)
            firstStory = body['stories'][0]
            self.assertEqual(firstStory['id'], 1)
            self.assertEqual(firstStory['text'], 'Trial story of example admin user :)')
            self.assertEqual(firstStory['dicenumber'], None)
            self.assertEqual(firstStory['like'], 42)
            self.assertEqual(firstStory['dislike'], None)
            self.assertEqual(firstStory['author_id'], 1)




            # post a new story
            roll = json.dumps(["bird", "whale", "coffee", "bananas", "ladder", "glasses"])

            text = ""
            for i in range(0, 2000):
                text = text + " a"

            reply = client.post('/stories?userid=1', data=dict(text=text, roll=roll))


            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], -4)
            self.assertEqual(body['message'], "The story is too long. The length is > 1000 characters.")
            self.assertEqual(len(body['stories']), 1)
            firstStory = body['stories'][0]
            self.assertEqual(firstStory['id'], 1)
            self.assertEqual(firstStory['text'], 'Trial story of example admin user :)')
            self.assertEqual(firstStory['dicenumber'], None)
            self.assertEqual(firstStory['like'], 42)
            self.assertEqual(firstStory['dislike'], None)
            self.assertEqual(firstStory['author_id'], 1)




            # check database entry
            q = db.session.query(Story).order_by(Story.id.desc()).first()
            self.assertNotEqual(q.text,text)


            # logout
            reply = client.post('/logout',
                                data=json.dumps({
                                "email": "example@example.com",
                                "password": 'admin'}), content_type='application/json')

            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['response'], True)
            self.assertEqual(body['user_id'], 1)



    def test_invalid_post_wrong_parameters(self):




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

            self.assertEqual(reply.status_code, 200)
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['response'], True)
            self.assertEqual(body['user_id'], 1)




            reply = client.get('/stories')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 1)
            self.assertEqual(len(body['stories']), 1)
            firstStory = body['stories'][0]
            self.assertEqual(firstStory['id'], 1)
            self.assertEqual(firstStory['text'], 'Trial story of example admin user :)')
            self.assertEqual(firstStory['dicenumber'], None)
            self.assertEqual(firstStory['like'], 42)
            self.assertEqual(firstStory['dislike'], None)
            self.assertEqual(firstStory['author_id'], 1)




            reply = client.post('/stories?userid=1')


            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], -8)
            self.assertEqual(body['message'], "Wrong parameters")


            # logout
            reply = client.post('/logout',
                                data=json.dumps({
                                "email": "example@example.com",
                                "password": 'admin'}), content_type='application/json')

            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['response'], True)
            self.assertEqual(body['user_id'], 1)



    def test_invalid_post_wrong_format_user(self):




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

            self.assertEqual(reply.status_code, 200)
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['response'], True)
            self.assertEqual(body['user_id'], 1)




            reply = client.get('/stories')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 1)
            self.assertEqual(len(body['stories']), 1)
            firstStory = body['stories'][0]
            self.assertEqual(firstStory['id'], 1)
            self.assertEqual(firstStory['text'], 'Trial story of example admin user :)')
            self.assertEqual(firstStory['dicenumber'], None)
            self.assertEqual(firstStory['like'], 42)
            self.assertEqual(firstStory['dislike'], None)
            self.assertEqual(firstStory['author_id'], 1)




            reply = client.post('/stories')


            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], -9)
            self.assertEqual(body['message'], "The userid is None")


            # logout
            reply = client.post('/logout',
                                data=json.dumps({
                                "email": "example@example.com",
                                "password": 'admin'}), content_type='application/json')

            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['response'], True)
            self.assertEqual(body['user_id'], 1)



if __name__ == '__main__':
    unittest.main()