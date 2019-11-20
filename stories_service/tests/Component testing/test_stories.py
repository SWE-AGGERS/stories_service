from stories_service.views import check_stories as cs
from stories_service.views.check_stories import TooSmallStoryError
from stories_service.views.check_stories import WrongFormatDiceError
from stories_service.views.check_stories import WrongFormatStoryError
from stories_service.views.check_stories import InvalidStory
import unittest
 
class TestStory(unittest.TestCase):
 
    def test_valid_story(self):
        die0 = 'bike moonandstars bag bird crying angry'
        die1 = 'tulip mouth caravan clock whale drink'
        die2 = 'happy coffee plate bus letter paws'
        die3 = 'cat pencil baloon bananas phone icecream'
        die4 = 'ladder car fire bang hat hamburger'
        die5 = 'rain heart glasses poo ball sun'
        storySet = die0 + " " + die1 + " " + die2 + " " + die3 + " " + die4 + " " + die5
        roll = ['bike','tulip','happy','cat','ladder','rain']
        self.assertEqual(cs.check_storyV2(storySet,roll),None)


        """

        r = requests.get('/dice')

        json_data = r.json()
        text = json_data['text']
        roll = json_data['roll']
        self.assertEqual(cs.check_storyV2(text, roll), None)
        
        """


    def test_invalid_story(self):
        storySet = ""
        for elem in range(0,30):
            string = "a"
            storySet = storySet + string + " "
        roll = ['bike', 'tulip', 'happy', 'cat', 'ladder', 'rain']
        with self.assertRaises(InvalidStory):
            cs.check_storyV2(storySet, roll)



    def test_invalid_story_wrong_type_story(self):
        roll = ['bike']
        with self.assertRaises(WrongFormatStoryError):
            cs.check_storyV2(122, roll)


    def test_invalid_story_short_story(self):
        die0 = 'bike moonandstars bag bird crying angry'
        die1 = 'tulip mouth caravan clock whale drink'
        die2 = 'happy coffee plate bus letter paws'
        die3 = 'cat pencil baloon bananas phone icecream'
        die4 = 'ladder car fire bang hat hamburger'
        die5 = 'rain heart glasses poo ball sun'
        storySet = ""
        roll = ['bike', 'tulip', 'happy', 'cat', 'ladder', 'rain']
        self.assertRaises(TooSmallStoryError, cs.check_storyV2,storySet,roll)



    def test_invalid_story_wrong_type_diceset(self):
        storySet = "a b c"
        roll = "a"
        self.assertRaises(WrongFormatDiceError, cs.check_storyV2,storySet,roll)












 
 
if __name__ == '__main__':
    unittest.main()