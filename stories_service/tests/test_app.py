import unittest
from stories_service.app import create_app
import sys


_app = None

class Test_app(unittest.TestCase):



    def test_restart_db_tables(self):

        global _app
        tested_app = create_app(debug=True)

        self.assertEqual(tested_app.config['WTF_CSRF_SECRET_KEY'], "A SECRET KEY")
        self.assertEqual(tested_app.config['SECRET_KEY'],'ANOTHER ONE')
        self.assertEqual(tested_app.config['SQLALCHEMY_DATABASE_URI'], 'sqlite:///storytellers.db')
        self.assertEqual(tested_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'], False)
        self.assertEqual(tested_app.config['SQLALCHEMY_ECHO'], False)
        self.assertEqual(tested_app.config['TESTING'], True)
        self.assertEqual(tested_app.config['LOGIN_DISABLED'], False)
        self.assertEqual(tested_app.config['WTF_CSRF_ENABLED'], True)





