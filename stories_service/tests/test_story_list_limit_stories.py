import unittest
from unittest import mock
import json
from stories_service.app import create_app
from stories_service.database import db
from stories_service.restart_db import restart_db_tables


_app = None

class Story_list_limit(unittest.TestCase):

    def test_story_list_limit_positive(self):

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



                    reply = client.get('/story_list/1/1')
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], 1)
                    self.assertEqual(body['message'], 'Here are the stories written by the user')



    def test_story_list_limit_negative(self):

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



                    reply = client.get('/story_list/4/1')
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], 0)
                    self.assertEqual(body['message'], 'No story has been found')



    def test_story_list_limit_negative_user_service_timeout(self):

        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            with mock.patch('stories_service.views.stories.send_request_user_service') as user_request_mock:
                user_request_mock.return_value = -2

                with mock.patch(
                        'stories_service.views.stories.send_request_reactions_service') as reactions_request_mock:
                    reactions_request_mock.return_value = 1



                    reply = client.get('/story_list/1/1')
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], -2)
                    self.assertEqual(body['message'], 'Timeout: the user service is not responding')


    def test_story_list_limit_negative_user_does_not_exists(self):

        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            with mock.patch('stories_service.views.stories.send_request_user_service') as user_request_mock:
                user_request_mock.return_value = -1

                with mock.patch(
                        'stories_service.views.stories.send_request_reactions_service') as reactions_request_mock:
                    reactions_request_mock.return_value = 1



                    reply = client.get('/story_list/1/1')
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], -1)
                    self.assertEqual(body['message'], 'The user does not exists')



    def test_story_list_limit_negative_reactions_service_timeout(self):

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



                    reply = client.get('/story_list/1/1')
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], -4)
                    self.assertEqual(body['message'], 'Timeout: the reactions service is not responding')



    def test_story_list_limit_negative_reactions_service_problems(self):

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



                    reply = client.get('/story_list/1/1')
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], -3)
                    self.assertEqual(body['message'], 'One or more of the stories written by the user does not exists in the reaction database')


    def test_story_list_limit_negative_wrong_limit(self):

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



                    reply = client.get('/story_list/1/0')
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], -5)
                    self.assertEqual(body['message'], 'limit < 1')
