import unittest
from stories_service.app import create_app
from stories_service.database import db, Story
from flask import json, jsonify
from stories_service.restart_db import restart_db_tables
from unittest import mock




class TestDeleteStory(unittest.TestCase):

    def test_delete_story_negative_timeout_user_service(self):

        tested_app = create_app(debug=True)
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            with mock.patch('stories_service.views.stories.send_request_user_service') as user_request_mock:
                user_request_mock.return_value = -2

                reply = client.post('/stories/remove/1?userid=1')
                self.assertEqual(reply.status_code, 200)
                body = json.loads(str(reply.data, 'utf8'))
                self.assertEqual(body['result'], -3)
                self.assertEqual(body['message'], 'Timeout: the user service is not responding')



    def test_delete_story_negative_user_not_registered(self):

        tested_app = create_app(debug=True)
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            with mock.patch('stories_service.views.stories.send_request_user_service') as user_request_mock:
                user_request_mock.return_value = -1

                reply = client.post('/stories/remove/1?userid=1')
                self.assertEqual(reply.status_code, 200)
                body = json.loads(str(reply.data, 'utf8'))
                self.assertEqual(body['result'], -4)
                self.assertEqual(body['message'], 'The user does not exists')


    def test_delete_story_positive(self):

        tested_app = create_app(debug=True)
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            with mock.patch('stories_service.views.stories.send_request_user_service') as user_request_mock:
                user_request_mock.return_value = 1

                reply = client.post('/stories/remove/1?userid=1')
                self.assertEqual(reply.status_code, 200)
                body = json.loads(str(reply.data, 'utf8'))
                self.assertEqual(body['result'], 1)
                self.assertEqual(body['message'], 'Story removed')



    def test_delete_story_negative_wrong_story(self):

        tested_app = create_app(debug=True)
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            with mock.patch('stories_service.views.stories.send_request_user_service') as user_request_mock:
                user_request_mock.return_value = 1

                reply = client.post('/stories/remove/2?userid=1')
                self.assertEqual(reply.status_code, 200)
                body = json.loads(str(reply.data, 'utf8'))
                self.assertEqual(body['result'], -1)
                self.assertEqual(body['message'], 'The story you want to delete does not exist')


    def test_delete_story_negative_story_written_by_another_user(self):

        tested_app = create_app(debug=True)
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            with mock.patch('stories_service.views.stories.send_request_user_service') as user_request_mock:
                user_request_mock.return_value = 1

                with mock.patch('stories_service.views.stories.send_request_reactions_service') as reactions_request_mock:
                    reactions_request_mock.return_value = 1

                    # post a new story

                    roll = ["bird", "whale", "coffee", "bananas", "ladder", "glasses"]
                    reply = client.post('/stories?userid=2', data=json.dumps({'created_story': {
                                'text':"bird whale coffee bananas ladder glasses", 'roll': roll}}), content_type='application/json')
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], 1)
                    self.assertEqual(body['message'], "Story created")



                    reply = client.post('/stories/remove/2?userid=1')
                    self.assertEqual(reply.status_code, 200)
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(body['result'], 0)
                    self.assertEqual(body['message'], 'You cannot remove a story that was not written by you')



    def test_delete_story_negative_user_not_inserted(self):

        tested_app = create_app(debug=True)
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            with mock.patch('stories_service.views.stories.send_request_user_service') as user_request_mock:
                user_request_mock.return_value = 1

                reply = client.post('/stories/remove/1')
                self.assertEqual(reply.status_code, 200)
                body = json.loads(str(reply.data, 'utf8'))
                self.assertEqual(body['result'], -2)
                self.assertEqual(body['message'], 'userid not inserted')

