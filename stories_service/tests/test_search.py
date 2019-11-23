import unittest
import json
from stories_service.app import create_app
from stories_service.database import db
from stories_service.restart_db import restart_db_tables


_app = None

class SearchTestCase(unittest.TestCase):

    def test_search_story(self):


        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            reply = client.post('/login',
                                data=json.dumps({"email": 'example@example.com', 'password': 'admin'}),
                                content_type='application/json')


            self.assertEqual(reply.status_code, 200)
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['response'], True)
            self.assertEqual(body['user_id'], 1)

            reply = client.get('/search_story',
                               data = json.dumps({"story": {"text": 'example'}}),
                               content_type = 'application/json')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 1)

    def test_search_story_negative(self):

        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            reply = client.post('/login',
                                data=json.dumps({"email": 'example@example.com', 'password': 'admin'}),
                                content_type='application/json')

            self.assertEqual(reply.status_code, 200)
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['response'], True)
            self.assertEqual(body['user_id'], 1)

            reply = client.get('/search_story',
                               data = json.dumps({"story": {"text": 'prova'}}),
                               content_type = 'application/json')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 0)


    def test_search_story_error_text_none(self):


        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            reply = client.post('/login',
                                data=json.dumps({"email": 'example@example.com', 'password': 'admin'}),
                                content_type='application/json')


            self.assertEqual(reply.status_code, 200)
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['response'], True)
            self.assertEqual(body['user_id'], 1)

            reply = client.get('/search_story')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], -2)




    def test_search_story_error_text_empty(self):


        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)



        with tested_app.test_client() as client:

            reply = client.post('/login',
                                data=json.dumps({"email": 'example@example.com', 'password': 'admin'}),
                                content_type='application/json')


            self.assertEqual(reply.status_code, 200)
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['response'], True)
            self.assertEqual(body['user_id'], 1)

            reply = client.get('/search_story',
                               data = json.dumps({"story": {"text": ''}}),
                               content_type = 'application/json')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], -1)


    def test_search_story_error_text_empty_v2(self):


        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)



        with tested_app.test_client() as client:

            reply = client.post('/login',
                                data=json.dumps({"email": 'example@example.com', 'password': 'admin'}),
                                content_type='application/json')


            self.assertEqual(reply.status_code, 200)
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['response'], True)
            self.assertEqual(body['user_id'], 1)

            reply = client.get('/search_story',
                               data=json.dumps({"story": {"text": ' '}}),
                               content_type='application/json')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], -1)



