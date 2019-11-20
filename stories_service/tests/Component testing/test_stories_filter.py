import unittest
import json
from stories_service.app import create_app
from stories_service.database import Story, db
from stories_service.tests.restart_db import restart_db_tables

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
            self.assertEqual(body['result'], 1)


            # Filter correctly a time interval
            reply = client.post('/stories/filter', data=json.dumps({
                'init_date': '2019-01-01',
                'end_date': '2019-12-01',
            }), )
            self.assertEqual(reply.status_code, 200)
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 0)
            self.assertIn(b'Trial story of example', body['stories'])



            # Filter wrongly a time interval (init_date > end_date)
            reply = client.post('/stories/filter', data=json.dumps({
                'init_date': '2019-12-01',
                'end_date': '2019-01-01',
            }))
            self.assertEqual(reply.status_code, 200)
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], -1)
            #self.assertIn(b'Cant travel back in time', reply.data)


            # Filter correctly a time interval with no stories
            reply = client.post('/stories/filter', data=json.dumps({
                'init_date': '2017-01-01',
                'end_date': '2017-12-01',
            }), )
            self.assertEqual(reply.status_code, 404)





    def test2(self):
        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        # create 100 Stories
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

