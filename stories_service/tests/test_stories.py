from stories_service.views import check_stories as cs
from stories_service.views.check_stories import TooSmallStoryError
from stories_service.views.check_stories import WrongFormatDiceError
from stories_service.views.check_stories import WrongFormatStoryError
from stories_service.views.check_stories import InvalidStory
from stories_service.views.check_stories import WrongFormatSingleDiceError
from stories_service.views.check_stories import TooLongStoryError
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



    def test_invalid_story(self):
        storySet = ""
        for elem in range(0,30):
            string = "a"
            storySet = storySet + string + " "
        roll = ['bike', 'tulip', 'happy', 'cat', 'ladder', 'rain']


        with self.assertRaises(InvalidStory) as cm:
            cs.check_storyV2(storySet, roll)
        err = cm.exception
        self.assertEqual(str(err), 'Invalid story')



    def test_invalid_story_wrong_type_story(self):


        roll = ['bike']
        with self.assertRaises(WrongFormatStoryError) as cm:
            cs.check_storyV2(122, roll)
        err = cm.exception
        self.assertEqual(str(err), "The story must be a string.")



    def test_invalid_story_short_story(self):


        storySet = ""
        roll = ['bike', 'tulip', 'happy', 'cat', 'ladder', 'rain']

        with self.assertRaises(TooSmallStoryError) as cm:
            cs.check_storyV2(storySet,roll)
        err = cm.exception
        self.assertEqual(str(err), "The number of words of the story must greater or equal of the number of resulted faces.")




    def test_invalid_story_long_story(self):


        storySet = ""
        for elem in range(0,2000):
            storySet = storySet + "a "

        roll = ['bike', 'tulip', 'happy', 'cat', 'ladder', 'rain']

        with self.assertRaises(TooLongStoryError) as cm:
            cs.check_storyV2(storySet,roll)
        err = cm.exception
        self.assertEqual(str(err), "The story is too long. The length is > 1000 characters.")





    def test_invalid_story_wrong_type_diceset(self):


        storySet = "a b c"
        roll = "a"

        with self.assertRaises(WrongFormatDiceError) as cm:
            cs.check_storyV2(storySet,roll)
        err = cm.exception
        self.assertEqual(str(err), "The dice set must be a list.")


    def test_invalid_story_wrong_format_single_dice_error(self):


        die0 = 'bike moonandstars bag bird crying angry'
        die1 = 'tulip mouth caravan clock whale drink'
        die2 = 'happy coffee plate bus letter paws'
        die3 = 'cat pencil baloon bananas phone icecream'
        die4 = 'ladder car fire bang hat hamburger'
        die5 = 'rain heart glasses poo ball sun'
        storySet = die0 + " " + die1 + " " + die2 + " " + die3 + " " + die4 + " " + die5
        roll = ['bike','tulip','happy','cat','ladder',1]


        with self.assertRaises(WrongFormatSingleDiceError) as cm:
            cs.check_storyV2( storySet, roll)
        err = cm.exception
        self.assertEqual(str(err), "Every dice of the dice set must be a die.")








if __name__ == '__main__':
    unittest.main()