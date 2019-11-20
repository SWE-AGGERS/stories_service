import unittest
import json
from stories_service.app import create_app
from stories_service.database import db, Story
from stories_service.tests.restart_db import restart_db_tables

_app = None

class TestNewStory(unittest.TestCase):
    def test_get_stories_at_least_one_story(self):

        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            reply = client.get('/stories')

            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 1)
            self.assertEqual(len(body['stories']), 1)
            firstStory = body['stories'][0]
            self.assertEqual(firstStory['id'], 1)
            self.assertEqual(firstStory['text'], 'Trial story of example admin user :)')
            self.assertEqual(firstStory['dicenumber'], None)
            self.assertEqual(firstStory['like'], 42)
            self.assertEqual(firstStory['dislike'], None)
            self.assertEqual(firstStory['author_id'], 1)





    def test_get_stories_no_story(self):

        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)



        with tested_app.test_client() as client:

            reply = client.get('/stories/remove/1')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 1)


            reply = client.get('/stories')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['result'], 0)
            
            
            


