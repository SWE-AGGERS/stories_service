import unittest
from unittest import mock
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

            with mock.patch('stories_service.views.stories.send_request_user_service') as user_request_mock:
                user_request_mock.return_value = 1

                with mock.patch(
                        'stories_service.views.stories.send_request_reactions_service') as reactions_request_mock:
                    reactions_request_mock.return_value = 1



                    reply = client.get('/search_story',
                                       data = json.dumps({"story": {"text": 'example'}}),
                                       content_type = 'application/json')
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], 1)
                    self.assertEqual(body['message'], "At least one story has been found")


    def test_search_story_negative(self):

        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            with mock.patch('stories_service.views.stories.send_request_user_service') as user_request_mock:
                user_request_mock.return_value = 1

                with mock.patch(
                        'stories_service.views.stories.send_request_reactions_service') as reactions_request_mock:
                    reactions_request_mock.return_value = 1



                    reply = client.get('/search_story',
                                       data = json.dumps({"story": {"text": 'no'}}),
                                       content_type = 'application/json')
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], 0)
                    self.assertEqual(body['message'], "No story has been found")


    def test_search_story_error_text_none(self):


            global _app
            if _app is None:
                tested_app = create_app(debug=True)
                _app = tested_app
            else:
                tested_app = _app
            restart_db_tables(db, tested_app)

            with tested_app.test_client() as client:

                with mock.patch('stories_service.views.stories.send_request_user_service') as user_request_mock:
                    user_request_mock.return_value = 1

                    with mock.patch(
                            'stories_service.views.stories.send_request_reactions_service') as reactions_request_mock:
                        reactions_request_mock.return_value = 1

                        reply = client.get('/search_story')
                        body = json.loads(str(reply.data, 'utf8'))
                        self.assertEqual(reply.status_code, 200)
                        self.assertEqual(body['result'], -2)
                        self.assertEqual(body['message'], "Story empty")




    def test_search_story_error_text_empty(self):


        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            with mock.patch('stories_service.views.stories.send_request_user_service') as user_request_mock:
                user_request_mock.return_value = 1

                with mock.patch(
                        'stories_service.views.stories.send_request_reactions_service') as reactions_request_mock:
                    reactions_request_mock.return_value = 1



                    reply = client.get('/search_story',
                                       data = json.dumps({"story": {"text": ''}}),
                                       content_type = 'application/json')
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], -1)
                    self.assertEqual(body['message'], "The text inserted is empty")



    def test_search_story_error_text_empty_v2(self):


        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            with mock.patch('stories_service.views.stories.send_request_user_service') as user_request_mock:
                user_request_mock.return_value = 1

                with mock.patch(
                        'stories_service.views.stories.send_request_reactions_service') as reactions_request_mock:
                    reactions_request_mock.return_value = 1



                    reply = client.get('/search_story',
                                       data = json.dumps({"story": {"text": ' '}}),
                                       content_type = 'application/json')
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], -1)
                    self.assertEqual(body['message'], "The text inserted is empty")





    def test_search_story_reactions_service_timeout(self):

        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            with mock.patch('stories_service.views.stories.send_request_user_service') as user_request_mock:
                user_request_mock.return_value = 1

                with mock.patch(
                        'stories_service.views.stories.send_request_reactions_service') as reactions_request_mock:
                    reactions_request_mock.return_value = -1



                    reply = client.get('/search_story',
                                       data = json.dumps({"story": {"text": 'example'}}),
                                       content_type = 'application/json')
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], -4)
                    self.assertEqual(body['message'], "Timeout: the reactions service is not responding")



    def test_search_story_reactions_service_problem(self):

        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            with mock.patch('stories_service.views.stories.send_request_user_service') as user_request_mock:
                user_request_mock.return_value = 1

                with mock.patch(
                        'stories_service.views.stories.send_request_reactions_service') as reactions_request_mock:
                    reactions_request_mock.return_value = -2



                    reply = client.get('/search_story',
                                       data = json.dumps({"story": {"text": 'example'}}),
                                       content_type = 'application/json')
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], -3)
                    self.assertEqual(body['message'], "One or more of the stories does not exists in the reaction database")
