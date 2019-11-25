import unittest
from unittest import mock
from stories_service.app import create_app
from stories_service.database import db, Story
from stories_service.restart_db import restart_db_tables
import json
from stories_service.views.stories import serializeble_story
import datetime

_app = None

class TestRandomStory(unittest.TestCase):



    """

    def test_story_retrieval(self):

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

                with mock.patch('stories_service.views.stories.send_request_reactions_service') as reactions_request_mock:
                    reactions_request_mock.return_value = 1


                    reply = client.get('/stories/random')
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], 1)
                    self.assertEqual(body['message'], 'The story exists')
                    randomStory = body['story']
                    self.assertEqual(randomStory['id'], 1)
                    self.assertEqual(randomStory['text'], 'Trial story of example admin user :)')
                    self.assertEqual(randomStory['dicenumber'], None)
                    self.assertEqual(randomStory['like'], 42)
                    self.assertEqual(randomStory['dislike'], None)
                    self.assertEqual(randomStory['author_id'], 1)
    """

    def test_no_story(self):

        tested_app = create_app(debug=True)
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            with mock.patch('stories_service.views.stories.send_request_user_service') as user_request_mock:
                user_request_mock.return_value = 1

                with mock.patch('stories_service.views.stories.send_request_reactions_service') as reactions_request_mock:
                    reactions_request_mock.return_value = 1

                    reply = client.post('/stories/remove/1?userid=1')
                    self.assertEqual(reply.status_code, 200)
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(body['result'], 1)
                    self.assertEqual(body['message'], 'Story removed')


                    reply = client.get('/stories/random')
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], 0)
                    self.assertEqual(body['message'], 'The story does not exists')





    def test_reactions_service_problem(self):


        tested_app = create_app(debug=True)
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            with mock.patch('stories_service.views.stories.send_request_user_service') as user_request_mock:
                user_request_mock.return_value = 1

                with mock.patch('stories_service.views.stories.send_request_reactions_service') as reactions_request_mock:
                    reactions_request_mock.return_value = -2



                    reply = client.get('/stories/random')
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], -1)
                    self.assertEqual(body['message'], 'The story does not exists in the reaction database')






    def test_reactions_service_timeout(self):

        tested_app = create_app(debug=True)
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            with mock.patch('stories_service.views.stories.send_request_user_service') as user_request_mock:
                user_request_mock.return_value = 1

                with mock.patch('stories_service.views.stories.send_request_reactions_service') as reactions_request_mock:
                    reactions_request_mock.return_value = -1



                    reply = client.get('/stories/random')
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], -2)
                    self.assertEqual(body['message'], 'Timeout: the reactions service is not responding')


