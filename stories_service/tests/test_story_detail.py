import unittest
from unittest import mock
import json
from stories_service.app import create_app
from stories_service.database import Story, db
from stories_service.restart_db import restart_db_tables

_app = None

class TestApp(unittest.TestCase):


    """

    def test_story_detail_positive(self):


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



                    reply = client.get('/stories/1')
                    self.assertEqual(reply.status_code, 200)
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(body['result'], 1)
                    self.assertEqual(body['message'], 'The story exists')

    """


    def test_story_detail_negative(self):

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



                    reply = client.get('/stories/100')
                    self.assertEqual(reply.status_code, 200)
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(body['result'], 0)
                    self.assertEqual(body['message'], 'The story does not exists')


    def test_story_detail_reactions_service_problem(self):

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



                    reply = client.get('/stories/1')
                    self.assertEqual(reply.status_code, 200)
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(body['result'], -1)
                    self.assertEqual(body['message'], 'The story does not exists in the reaction database')



    def test_story_detail_reactions_service_timeout(self):

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



                    reply = client.get('/stories/1')
                    self.assertEqual(reply.status_code, 200)
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(body['result'], -2)
                    self.assertEqual(body['message'], 'Timeout: the reactions service is not responding')

