import unittest
from unittest import mock
import json
from stories_service.app import create_app
from stories_service.database import db, Story
from stories_service.restart_db import restart_db_tables
import sys

_app = None

class TestNewStory(unittest.TestCase):




    def test_valid_post(self):




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

                    
                    # post a new story

                    roll = ["bird", "whale", "coffee", "bananas", "ladder", "glasses"]
                    reply = client.post('/stories?userid=1', data=json.dumps({'created_story': {
                        'text': "bird whale coffee bananas ladder glasses", 'roll': roll}}), content_type='application/json')
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], 1)
                    self.assertEqual(body['message'], "Story created")




                    # check database entry
                    q = db.session.query(Story).order_by(Story.id.desc()).first()
                    self.assertEqual(q.text, "bird whale coffee bananas ladder glasses")
                    self.assertEqual(q.dicenumber, 6)







    def test_invalid_post(self):




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


                    # post a new story

                    roll = ["bird", "whale", "coffee", "bananas", "ladder", "glasses"]
                    reply = client.post('/stories?userid=1', data=json.dumps({'created_story': {
                        'text': "Just a new story for test purposes!", 'roll': roll}}), content_type='application/json')
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], -6)
                    self.assertEqual(body['message'], "Invalid story. Try again!")

                    # check database entry
                    q = db.session.query(Story).order_by(Story.id.desc()).first()
                    self.assertNotEqual(q.text, "bird whale coffee bananas ladder glasses")






    def test_invalid_post_short_story(self):


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


                    # post a new story

                    roll = ["bird", "whale", "coffee", "bananas", "ladder", "glasses"]
                    reply = client.post('/stories?userid=1', data=json.dumps({'created_story': {
                        'text': "short story", 'roll': roll}}), content_type='application/json')
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], -5)
                    self.assertEqual(body['message'], "The number of words of the story must greater or equal of the number of resulted faces.")

                    # check database entry
                    q = db.session.query(Story).order_by(Story.id.desc()).first()
                    self.assertNotEqual(q.text, "bird whale coffee bananas ladder glasses")




    def test_invalid_post_too_long_story(self):


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


                    # post a new story

                    text = ""
                    for i in range(0, 2000):
                        text = text + " a"


                    roll = ["bird", "whale", "coffee", "bananas", "ladder", "glasses"]
                    reply = client.post('/stories?userid=1', data=json.dumps({'created_story': {
                        'text': text, 'roll': roll}}), content_type='application/json')
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], -4)
                    self.assertEqual(body['message'], "The story is too long. The length is > 1000 characters.")

                    # check database entry
                    q = db.session.query(Story).order_by(Story.id.desc()).first()
                    self.assertNotEqual(q.text, "bird whale coffee bananas ladder glasses")



    def test_invalid_post_wrong_parameters(self):


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



                    # post a new story

                    reply = client.post('/stories?userid=1')

                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], -8)
                    self.assertEqual(body['message'], "Wrong parameters")



    def test_invalid_post_wrong_parameters_text(self):


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



                    # post a new story

                    roll = ["bird", "whale", "coffee", "bananas", "ladder", "glasses"]

                    reply = client.post('/stories?userid=1', data=json.dumps({'created_story': {
                        'roll': roll}}), content_type='application/json')

                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], -8)
                    self.assertEqual(body['message'], "Wrong parameters")



    def test_invalid_post_wrong_parameters_roll(self):


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



                    # post a new story

                    reply = client.post('/stories?userid=1', data=json.dumps({'created_story': {
                        'text': "bird whale coffee bananas ladder glasses"}}),
                                        content_type='application/json')

                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], -8)
                    self.assertEqual(body['message'], "Wrong parameters")



    def test_invalid_post_wrong_format_user(self):


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


                    # post a new story

                    reply = client.post('/stories')

                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], -9)
                    self.assertEqual(body['message'], "The userid is None")

    def test_timeout_user_service(self):

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

                    # post a new story

                    roll = ["bird", "whale", "coffee", "bananas", "ladder", "glasses"]
                    reply = client.post('/stories?userid=1', data=json.dumps({'created_story': {
                        'text': "bird whale coffee bananas ladder glasses", 'roll': roll}}),
                                        content_type='application/json')
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], -7)
                    self.assertEqual(body['message'], "Timeout: the user service is not responding")

                    # check database entry
                    q = db.session.query(Story).order_by(Story.id.desc()).first()
                    self.assertNotEqual(q.text, "bird whale coffee bananas ladder glasses")


    def test_timeout_user_does_not_exists(self):

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

                    # post a new story

                    roll = ["bird", "whale", "coffee", "bananas", "ladder", "glasses"]
                    reply = client.post('/stories?userid=1', data=json.dumps({'created_story': {
                        'text': "bird whale coffee bananas ladder glasses", 'roll': roll}}),
                                        content_type='application/json')
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], 0)
                    self.assertEqual(body['message'], "The user does not exists")

                    # check database entry
                    q = db.session.query(Story).order_by(Story.id.desc()).first()
                    self.assertNotEqual(q.text, "bird whale coffee bananas ladder glasses")




    def test_timeout_reactions_service(self):

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

                    # post a new story

                    roll = ["bird", "whale", "coffee", "bananas", "ladder", "glasses"]
                    reply = client.post('/stories?userid=1', data=json.dumps({'created_story': {
                        'text': "bird whale coffee bananas ladder glasses", 'roll': roll}}),
                                        content_type='application/json')
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], -11)
                    self.assertEqual(body['message'], "Timeout: the reactions service is not responding")

                    # check database entry
                    q = db.session.query(Story).order_by(Story.id.desc()).first()
                    self.assertNotEqual(q.text, "bird whale coffee bananas ladder glasses")




    def test_reactions_service_story_not_found(self):

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

                    # post a new story

                    roll = ["bird", "whale", "coffee", "bananas", "ladder", "glasses"]
                    reply = client.post('/stories?userid=1', data=json.dumps({'created_story': {
                        'text': "bird whale coffee bananas ladder glasses", 'roll': roll}}),
                                        content_type='application/json')
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], -10)
                    self.assertEqual(body['message'], "One or more of the stories written by the user does not exists in the reaction database")

                    # check database entry
                    q = db.session.query(Story).order_by(Story.id.desc()).first()
                    self.assertNotEqual(q.text, "bird whale coffee bananas ladder glasses")

    def test_invalid_story_WrongFormatStoryError(self):

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

                    # post a new story

                    roll = ["bird", "whale", "coffee", "bananas", "ladder", "glasses"]
                    reply = client.post('/stories?userid=1', data=json.dumps({'created_story': {
                        'text': 1, 'roll': roll}}),
                                        content_type='application/json')
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], -1)
                    self.assertEqual(body['message'], "There was an error. Try again.")

                    # check database entry
                    q = db.session.query(Story).order_by(Story.id.desc()).first()
                    self.assertNotEqual(q.text, 1)


    def test_invalid_story_WrongFormatDiceError(self):

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

                    # post a new story

                    reply = client.post('/stories?userid=1', data=json.dumps({'created_story': {
                        'text': "bird whale coffee bananas ladder glasses", 'roll': 1}}),
                                        content_type='application/json')
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], -2)
                    self.assertEqual(body['message'], "There was an error. Try again.")

                    # check database entry
                    q = db.session.query(Story).order_by(Story.id.desc()).first()
                    self.assertNotEqual(q.text, 1)


    def test_invalid_story_WrongFormatSingleDiceError(self):

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

                    # post a new story

                    roll = ["bird", "whale", "coffee", "bananas", "ladder", 1]

                    reply = client.post('/stories?userid=1', data=json.dumps({'created_story': {
                        'text': "bird whale coffee bananas ladder glasses", 'roll': roll}}),
                                        content_type='application/json')
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], -3)
                    self.assertEqual(body['message'], "There was an error. Try again.")

                    # check database entry
                    q = db.session.query(Story).order_by(Story.id.desc()).first()
                    self.assertNotEqual(q.text, 1)

    def test_invalid_story_wrong_parameters_text_roll(self):

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

                    # post a new story

                    roll = ["bird", "whale", "coffee", "bananas", "ladder", "glasses"]
                    reply = client.post('/stories?userid=1', data=json.dumps({'created_story': {
                        'text': "bird whale coffee bananas ladder glasses", 'rolls': roll}}),
                                        content_type='application/json')


                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], -8)
                    self.assertEqual(body['message'], "Wrong parameters")



    def test_invalid_story_wrong_parameters_text_roll_None(self):

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

                    # post a new story

                    roll = ["bird", "whale", "coffee", "bananas", "ladder", "glasses"]
                    reply = client.post('/stories?userid=1', data=json.dumps({'created_story': {
                        'text': "bird whale coffee bananas ladder glasses", 'roll': None}}),
                                        content_type='application/json')


                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(reply.status_code, 200)
                    self.assertEqual(body['result'], -8)
                    self.assertEqual(body['message'], "Wrong parameters")


if __name__ == '__main__':
    unittest.main()