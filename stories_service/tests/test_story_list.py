import unittest
from unittest import mock
import json
from stories_service.app import create_app
from stories_service.database import db
from stories_service.restart_db import restart_db_tables


_app = None

class SearchTestCase(unittest.TestCase):

    def test_story_list_positive(self):

        tested_app = create_app(debug=True)
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            with mock.patch('stories_service.views.stories.send_request_user_service') as user_request_mock:
                user_request_mock.return_value = 1

                with mock.patch(
                        'stories_service.views.stories.send_request_reactions_service') as reactions_request_mock:
                    reactions_request_mock.return_value = 1



                    reply = client.get('/story_list/1')
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], 1)
                    self.assertEqual(body['message'], 'Here are the stories written by the user')



    def test_story_list_negative(self):

        tested_app = create_app(debug=True)
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            with mock.patch('stories_service.views.stories.send_request_user_service') as user_request_mock:
                user_request_mock.return_value = 1

                with mock.patch(
                        'stories_service.views.stories.send_request_reactions_service') as reactions_request_mock:
                    reactions_request_mock.return_value = 1



                    reply = client.get('/story_list/4')
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], 0)
                    self.assertEqual(body['message'], 'No story has been found')



    def test_story_list_negative_user_service_timeout(self):

        tested_app = create_app(debug=True)
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            with mock.patch('stories_service.views.stories.send_request_user_service') as user_request_mock:
                user_request_mock.return_value = -2

                with mock.patch(
                        'stories_service.views.stories.send_request_reactions_service') as reactions_request_mock:
                    reactions_request_mock.return_value = 1



                    reply = client.get('/story_list/1')
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], -2)
                    self.assertEqual(body['message'], 'Timeout: the user service is not responding')


    def test_story_list_negative_user_does_not_exists(self):

        tested_app = create_app(debug=True)
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            with mock.patch('stories_service.views.stories.send_request_user_service') as user_request_mock:
                user_request_mock.return_value = -1

                with mock.patch(
                        'stories_service.views.stories.send_request_reactions_service') as reactions_request_mock:
                    reactions_request_mock.return_value = 1



                    reply = client.get('/story_list/1')
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], -1)
                    self.assertEqual(body['message'], 'The user does not exists')



    def test_story_list_negative_reactions_service_timeout(self):

        tested_app = create_app(debug=True)
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            with mock.patch('stories_service.views.stories.send_request_user_service') as user_request_mock:
                user_request_mock.return_value = 1

                with mock.patch(
                        'stories_service.views.stories.send_request_reactions_service') as reactions_request_mock:
                    reactions_request_mock.return_value = -1



                    reply = client.get('/story_list/1')
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], -4)
                    self.assertEqual(body['message'], 'Timeout: the reactions service is not responding')



    def test_story_list_negative_reactions_service_problems(self):

        tested_app = create_app(debug=True)
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            with mock.patch('stories_service.views.stories.send_request_user_service') as user_request_mock:
                user_request_mock.return_value = 1

                with mock.patch(
                        'stories_service.views.stories.send_request_reactions_service') as reactions_request_mock:
                    reactions_request_mock.return_value = -2



                    reply = client.get('/story_list/1')
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], -3)
                    self.assertEqual(body['message'], 'One or more of the stories written by the user does not exists in the reaction database')