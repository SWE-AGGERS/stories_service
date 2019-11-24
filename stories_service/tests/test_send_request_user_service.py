import unittest
from stories_service.views.stories import send_request_user_service

_app = None

class Testsend_request_user_service(unittest.TestCase):




    def test_send_request_user_service(self):


        self.assertEqual(send_request_user_service(1), -2)




