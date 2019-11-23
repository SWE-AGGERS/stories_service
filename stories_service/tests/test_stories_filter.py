import unittest
from unittest import mock
import json
from stories_service.app import create_app
from stories_service.database import Story, db
from stories_service.restart_db import restart_db_tables

_app = None

class TestStoryFilter(unittest.TestCase):


    def test_filter_positive(self):



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



                    # Filter correctly a time interval
                    reply = client.post('/stories/filter', data=json.dumps({'info':
                        {'userid': 1,
                        'init_date': '2019-01-01',
                        'end_date': '2019-12-01',
                    }}),content_type = 'application/json')


                    self.assertEqual(reply.status_code, 200)
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(body['result'], 1)
                    self.assertEqual(body['message'], 'At least one story has been found')



    def test_filter_positive_no_stories(self):


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

                    # Filter correctly a time interval with no stories
                    reply = client.post('/stories/filter', data=json.dumps({'info':
                                                                                {'userid': 1,
                                                                                 'init_date': '2017-01-01',
                                                                                 'end_date': '2017-12-01',
                                                                                 }}),content_type = 'application/json')


                    self.assertEqual(reply.status_code, 200)
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(body['result'], 0)
                    self.assertEqual(body['message'], 'No story has been found')






    def test_filter_negative(self):



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

                    # Filter wrongly a time interval (init_date > end_date)
                    reply = client.post('/stories/filter', data=json.dumps({'info':
                                                                                {'userid': 1,
                                                                                 'init_date': '2019-12-01',
                                                                                 'end_date': '2019-01-01',
                                                                                 }}),content_type = 'application/json')


                    self.assertEqual(reply.status_code, 200)
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(body['result'], -1)
                    self.assertEqual(body['message'], 'The init date is greater than the end date')


    def test_filter_wrong_dates(self):


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

                    # Filter wrong dates

                    reply = client.post('/stories/filter', data=json.dumps({'info':
                                                                                {'userid': 1,
                                                                                 }}),content_type = 'application/json')


                    self.assertEqual(reply.status_code, 200)
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(body['result'], -2)
                    self.assertEqual(body['message'], 'Missing params')




    def test_filter_wrong_user(self):

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



                    # Filter correctly a time interval
                    reply = client.post('/stories/filter', data=json.dumps({'info':
                        { 'init_date': '2019-01-01',
                        'end_date': '2019-12-01',
                    }}),content_type = 'application/json')


                    self.assertEqual(reply.status_code, 200)
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(body['result'], -2)
                    self.assertEqual(body['message'], 'Missing params')



    def test_filter_user_service_timeout(self):



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



                    # Filter correctly a time interval
                    reply = client.post('/stories/filter', data=json.dumps({'info':
                        {'userid': 1,
                        'init_date': '2019-01-01',
                        'end_date': '2019-12-01',
                    }}),content_type = 'application/json')


                    self.assertEqual(reply.status_code, 200)
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(body['result'], -4)
                    self.assertEqual(body['message'], 'Timeout: the user service is not responding')


    def test_filter_user_does_not_exists(self):



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



                    # Filter correctly a time interval
                    reply = client.post('/stories/filter', data=json.dumps({'info':
                        {'userid': 1,
                        'init_date': '2019-01-01',
                        'end_date': '2019-12-01',
                    }}),content_type = 'application/json')


                    self.assertEqual(reply.status_code, 200)
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(body['result'], -5)
                    self.assertEqual(body['message'], 'The user does not exists')



    def test_filter_reactions_service_problems(self):



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



                    # Filter correctly a time interval
                    reply = client.post('/stories/filter', data=json.dumps({'info':
                        {'userid': 1,
                        'init_date': '2019-01-01',
                        'end_date': '2019-12-01',
                    }}),content_type = 'application/json')


                    self.assertEqual(reply.status_code, 200)
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(body['result'], -6)
                    self.assertEqual(body['message'], 'One or more of the stories written by the user does not exists in the reaction database')




    def test_filter_reactions_service_timeout(self):



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



                    # Filter correctly a time interval
                    reply = client.post('/stories/filter', data=json.dumps({'info':
                        {'userid': 1,
                        'init_date': '2019-01-01',
                        'end_date': '2019-12-01',
                    }}),content_type = 'application/json')


                    self.assertEqual(reply.status_code, 200)
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(body['result'], -7)
                    self.assertEqual(body['message'], 'Timeout: the reactions service is not responding')