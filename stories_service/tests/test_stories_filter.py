import unittest
import json
from stories_service.app import create_app
from stories_service.database import Story, db
from stories_service.restart_db import restart_db_tables

_app = None

class TestStoryFilter(unittest.TestCase):
    def test1(self):
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


            # Filter correctly a time interval
            reply = client.post('/stories/filter', data=json.dumps({ 'info':
                {'userid': 1,
                'init_date': '2019-01-01',
                'end_date': '2019-12-01',
            }}),)
            self.assertEqual(reply.status_code, 200)
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 1)
            self.assertEqual(len(body['stories']), 1)
            firstStory = body['stories'][0]
            self.assertEqual(firstStory['id'], 1)
            self.assertEqual(firstStory['text'], 'Trial story of example admin user :)')
            self.assertEqual(firstStory['dicenumber'], None)
            self.assertEqual(firstStory['like'], 42)
            self.assertEqual(firstStory['dislike'], None)
            self.assertEqual(firstStory['author_id'], 1)



            # Filter wrongly a time interval (init_date > end_date)
            reply = client.post('/stories/filter', data=json.dumps({ 'info':
                {'userid': 1,
                 'init_date': '2019-12-01',
                 'end_date': '2019-01-01',
            }}),)



            self.assertEqual(reply.status_code, 200)
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], -1)



            # Filter correctly a time interval with no stories
            reply = client.post('/stories/filter', data=json.dumps({ 'info':
                {'userid': 1,
                 'init_date': '2017-01-01',
                 'end_date': '2017-12-01',
            }}),)



            self.assertEqual(reply.status_code, 200)
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 0)

            # Filter wrong dates

            reply = client.post('/stories/filter', data=json.dumps({ 'info':
                {'userid': 1,
            }}),)



            self.assertEqual(reply.status_code, 200)
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], -2)

            # filter wrong user

            reply = client.post('/stories/filter', data=json.dumps({ 'info':
                {
                 'init_date': '2017-01-01',
                 'end_date': '2017-12-01',
            }}),)



            self.assertEqual(reply.status_code, 200)
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], -3)



