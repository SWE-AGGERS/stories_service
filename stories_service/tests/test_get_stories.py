import unittest
from unittest import mock
import json
from stories_service.app import create_app
from stories_service.database import db, Story
from stories_service.restart_db import restart_db_tables
import sys



class TestNewStory(unittest.TestCase):




    def test_get_stories_positive(self):




        tested_app = create_app(debug=True)
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            with mock.patch('stories_service.views.stories.send_request_user_service') as user_request_mock:
                user_request_mock.return_value = 1

                with mock.patch('stories_service.views.stories.send_request_reactions_service') as reactions_request_mock:
                    reactions_request_mock.return_value = 1

                    reply = client.get('/stories')
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], 1)
                    self.assertEqual(body['message'], 'Stories')



    def test_get_stories_negative(self):



        tested_app = create_app(debug=True)
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            with mock.patch('stories_service.views.stories.send_request_user_service') as user_request_mock:
                user_request_mock.return_value = 1

                with mock.patch('stories_service.views.stories.send_request_reactions_service') as reactions_request_mock:
                    reactions_request_mock.return_value = 1

                    # remove the story

                    reply = client.post('/stories/remove/1?userid=1')
                    self.assertEqual(reply.status_code, 200)
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(body['result'], 1)
                    self.assertEqual(body['message'], 'Story removed')

                    # return all stories: 0

                    reply = client.get('/stories')
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], 0)
                    self.assertEqual(body['message'], 'No stories')



    def test_get_stories_negative_reaction_service_timeout(self):




        tested_app = create_app(debug=True)
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            with mock.patch('stories_service.views.stories.send_request_user_service') as user_request_mock:
                user_request_mock.return_value = 1

                with mock.patch('stories_service.views.stories.send_request_reactions_service') as reactions_request_mock:
                    reactions_request_mock.return_value = -1

                    reply = client.get('/stories')
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], -2)
                    self.assertEqual(body['message'], 'Timeout: the reactions service is not responding')




    def test_get_stories_negative_reaction_service_problems(self):


        tested_app = create_app(debug=True)
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            with mock.patch('stories_service.views.stories.send_request_user_service') as user_request_mock:
                user_request_mock.return_value = 1

                with mock.patch('stories_service.views.stories.send_request_reactions_service') as reactions_request_mock:
                    reactions_request_mock.return_value = -2

                    reply = client.get('/stories')
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], -1)
                    self.assertEqual(body['message'], 'One or more of the stories written by the user does not exists in the reaction database')

