import unittest
from stories_service.app import create_app
from stories_service.database import db
from stories_service.tests.restart_db import restart_db_tables
import json

_app = None

class TestRandomStory(unittest.TestCase):
    def test_story_retrieval(self):

        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:


            # login
            reply = client.post('/login',
                             data=json.dumps({
                                "email": "example@example.com",
                                "password": 'admin'}), content_type='application/json')

            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['response'], True)
            self.assertEqual(body['user_id'], 1)

            reply = client.get('/stories/random')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body['story'], 'Trial story of example admin user')

            randomStory = body['story']
            self.assertEqual(randomStory['id'], 1)
            self.assertEqual(randomStory['text'], 'Trial story of example admin user :)')
            self.assertEqual(randomStory['dicenumber'], None)
            self.assertEqual(randomStory['like'], 42)
            self.assertEqual(randomStory['dislike'], None)
            self.assertEqual(randomStory['author_id'], 1)




if __name__ == '__main__':
    unittest.main()
