import unittest
import json
from stories_service.app import create_app
from stories_service.database import Story, db
from stories_service.restart_db import restart_db_tables

_app = None

class TestApp(unittest.TestCase):
    def test1(self):

        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:
            app = create_app().test_client()
            reply = app.get('/stories/1')
            self.assertEqual(reply.status_code, 200)
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 1)
            story = body['story']
            self.assertEqual(story['id'], 1)
            self.assertEqual(story['text'], 'Trial story of example admin user :)')
            self.assertEqual(story['dicenumber'], None)
            self.assertEqual(story['like'], 42)
            self.assertEqual(story['dislike'], None)
            self.assertEqual(story['author_id'], 1)

    def test2(self):

        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            app = create_app().test_client()
            reply = app.get('/stories/100')
            self.assertEqual(reply.status_code, 200)
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['result'], 0)
