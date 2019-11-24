import unittest
from stories_service.views.stories import send_request_reactions_service
from stories_service.database import Story




class Testsend_request_reactions_service(unittest.TestCase):




    def test_send_request_reactions_service_0_stories(self):


        arr = []
        allstories = []

        self.assertEqual(send_request_reactions_service(arr,allstories),1)


    def test_send_request_reactions_service_stories_none(self):


        arr = []


        self.assertEqual(send_request_reactions_service(arr,None),0)




    def test_send_request_reactions_service_one_story_timeout(self):


        arr = []

        example = Story()
        example.text = 'Trial story of example admin user :)'
        example.likes = 42
        example.author_id = 1
        example.dicenumber = 6
        example.roll = {'dice': ['bike', 'tulip', 'happy', 'cat', 'ladder', 'rain']}

        arr.append(example)

        self.assertEqual(send_request_reactions_service(arr,arr),-1)