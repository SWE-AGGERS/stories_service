import unittest
from stories_service.app import create_app
from stories_service.database import db, Story
from stories_service.restart_db import restart_db_tables, delete_all_db
import sys


_app = None

class Testdb(unittest.TestCase):



    def test_restart_db_tables(self):

        tested_app = create_app(debug=True)
        restart_db_tables(db, tested_app)


        self.assertEqual(restart_db_tables(db, tested_app), None)



    def test_delete_db(self):

        tested_app = create_app(debug=True)
        restart_db_tables(db, tested_app)

        self.assertEqual(delete_all_db(db, tested_app), None)