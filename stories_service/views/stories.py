from flask import jsonify
import json
from sqlalchemy import func
from flask import Blueprint, request
from stories_service.database import db, Story
from stories_service.views.check_stories import check_storyV2, InvalidStory, TooLongStoryError, TooSmallStoryError, WrongFormatDiceError, WrongFormatSingleDiceError, WrongFormatSingleFaceError, WrongFormatStoryError
import requests
from requests.exceptions import MissingSchema
from requests.exceptions import Timeout
import sys

stories = Blueprint('stories', __name__)

TIMEOUT = 5


@stories.route('/story_exists/<storyid>')
def story_exists(storyid):
    q = db.session.query(Story).filter_by(id=storyid)
    story = q.first()
    if story is not None:
        result = jsonify({"result": 1})
    else:
        result = jsonify({"result": 0})
    return result




@stories.route('/story_list/<userid>')
def story_list(userid):


    try:
        r = requests.get('/user_exists/' + userid, timeout=TIMEOUT)
    except Timeout:
        message = "Timeout: the user service is not responding"
        result = jsonify({"result": -2, "message": message})
        return result
    except MissingSchema:
        message = "The user service is offline"
        result = jsonify({"result": -3, "message": message})
        return result
    except Exception:
        message = "There was an error in the connection with the user service"
        result = jsonify({"result": -4, "message": message})
        return result

    json_data = r.json()
    user = json_data['result']
    if user != -1:
        stories = db.session.query(Story).filter(Story.author_id == userid)
        if stories is not None:
            result = jsonify({"result": 1, "stories": stories})
        else:
            result = jsonify({"result": 0})
        return result
    else:
        result = jsonify({"result": -1})
        return result









@stories.route('/stories', methods=['POST', 'GET'])
def get_stories():
    if 'POST' == request.method:

        # Verify that the user exists

        code = -1
        message = ""


        userid = request.args.get('userid')
        allstories = db.session.query.all()

        try:
            r = requests.get('/user_exists/'+userid,timeout=TIMEOUT)
        except Timeout:
            message = "Timeout: the user service is not responding"
            result = jsonify({"result": -7, "message": message,  "stories": allstories})
            return result
        except MissingSchema:
            message = "The user service is offline"
            result = jsonify({"result": -8, "message": message})
            return result
        except Exception:
            message = "There was an error in the connection with the user service"
            result = jsonify({"result": -9, "message": message})
            return result


        json_data = r.json()
        user = json_data['result']
        if user == -1:

            # if it does not exist I set the params accordingly

            code = 0
            message = "The user does not exists"
            result = jsonify({"result": code, "message": message, "stories": allstories})
            return result
        else:

            # otherwise I create the story and I verify that it is valid


            # Create a new story
            new_story = Story()
            new_story.author_id = userid
            new_story.likes = 0
            new_story.dislikes = 0



            # request of story and faces

            try:
                r = requests.get('/dice')
            except Timeout:
                message = "Timeout: the dice service is not responding"
                result = jsonify({"result": -10, "message": message,  "stories": allstories})
                return result
            except MissingSchema:
                message = "The dice service is offline"
                result = jsonify({"result": -11, "message": message})
                return result
            except Exception:
                message = "There was an error in the connection with the dice service"
                result = jsonify({"result": -12, "message": message})
                return result


            json_data = r.json()
            text = json_data['text']
            roll = json_data['roll']


            if (type(roll) is str):
                roll = roll.replace("[", "")
                roll = roll.replace("]", "")
                roll = roll.replace("'", "")
                roll = roll.replace(" ", "")
                aux = roll.split(",")
                roll = aux

            dicenumber = len(roll)
            try:
                check_storyV2(text, roll)
                new_story.text = text
                new_story.roll = {'dice': roll}
                new_story.dicenumber = dicenumber
                db.session.add(new_story)
                db.session.commit()
                code = 1
                message = "Story created"
            except WrongFormatStoryError:
                # print('ERROR 1', file=sys.stderr)
                code = -1
                message = "There was an error. Try again."

            except WrongFormatDiceError:
                # print('ERROR 2', file=sys.stderr)
                code = -2
                message = "There was an error. Try again."

            except WrongFormatSingleDiceError:
                # print('ERROR 5', file=sys.stderr)
                code = -3
                message = "There was an error. Try again."

            except TooLongStoryError:
                # print('ERROR 3', file=sys.stderr)
                code = -4
                message = "The story is too long. The length is > 1000 characters."

            except TooSmallStoryError:
                # print('ERROR 4', file=sys.stderr)
                code = -5
                message = "The number of words of the story must greater or equal of the number of resulted faces."



            except InvalidStory:
                # print('ERROR 6', file=sys.stderr)
                code = -6
                message = "Invalid story. Try again!"




        result = jsonify({"result": code, "message": message, "stories": allstories})
        return result





    elif 'GET' == request.method:
        result = []
        allstories = db.session.query(Story).all()
        if allstories is not None:
            for elem in allstories:
                result.append(serializeble_story(elem))
            #print(result, file=sys.stderr)
            return json.dumps({"result": 1, "stories": result})
        else:
            return json.dumps({"result": 0})





@stories.route('/stories/<storyid>', methods=['GET'])
def get_story_detail(storyid):
    q = db.session.query(Story).filter_by(id=storyid)
    story = q.first()
    if story is not None:
        result = json.dumps({"result": 1, "story": story})
    else:
        result = json.dumps({"result": 0})
    return result



"""

@stories.route('/rolldice/<dicenumber>/<dicesetid>', methods=['GET'])
def _roll(dicenumber, dicesetid):
    form = StoryForm()
    try:
        dice = DiceSet(dicesetid)
    except NonExistingSetError:
        abort(404)

    try:
        roll = dice.throw_dice(dicenumber)
        phrase = ""
        for elem in roll:
            phrase = phrase + elem + " "
    except WrongDiceNumberError:
        return _stories("<div class=\"alert alert-danger alert-dismissible fade show\">" +
                        "<button type=\"button\" class=\"close\" data-dismiss=\"alert\">&times;</button>" +
                        "<strong>Error!</strong> Wrong dice number!</div>")
    except WrongArgumentTypeError:
        return _stories("<div class=\"alert alert-danger alert-dismissible fade show\">" +
                        "<button type=\"button\" class=\"close\" data-dismiss=\"alert\">&times;</button>" +
                        "<strong>Error!</strong> Argument Dice number needs to be an integer!</div>")
    return render_template("create_story.html", form=form, set=dicesetid, roll=roll, phrase=phrase)



"""


@stories.route('/stories/random', methods=['GET'])
def random_story():
    q = db.session.query(Story).order_by(func.random()).limit(1)
    random_story_from_db = q.first()
    if random_story_from_db is not None:
        result = jsonify({"result": 1, "story": random_story_from_db})
    else:
        result = json.dumps({"result": 0})
    return result



@stories.route('/stories/filter', methods=['POST'])
def filter_stories():
    if request.method == 'POST':

        init_date = request.args.get('init_date')
        end_date = request.args.get('end_date')


        if init_date == None and end_date == None:
            message = "Wrong dates"
            result = jsonify({"result": -2, "message": message})
            return result

        if init_date > end_date:
            result = jsonify({"result": -1})
            return result


        f_stories = db.session.query(Story)\
            .filter(Story.date >= init_date)\
            .filter(Story.date <= end_date)\
            .all()


        if f_stories is not None:
            result = jsonify({'result': 1,"stories": f_stories})
        else:
            result = jsonify({"result": 0})
        return result








@stories.route('/stories/remove/<storyid>', methods=['POST'])
def remove_story(storyid):

    message = ""
    result = -1

    userid = request.args.get('userid')

    # Remove story
    q = db.session.query(Story).filter_by(id=storyid)
    story = q.first()
    if story is not None:
        if story.author_id == userid:

            try:
                r = requests.get("/user_exists"+userid)
            except Timeout:
                message = "Timeout: the user service is not responding"
                result = jsonify({"result": -3, "message": message})
                return result
            except MissingSchema:
                message = "The user service is offline"
                result = jsonify({"result": -4, "message": message})
                return result
            except Exception:
                message = "There was an error in the connection with the user service"
                result = jsonify({"result": -5, "message": message})
                return result

            json_data = r.json()
            code = json_data['result']
            if code:
                db.session.delete(story)
                db.session.commit()
                result = 1
                message = "Story removed"
            else:
                result = -0
                message = "There was a problem with the removal of the story. In particular in the deletion of the reactions"
        else:
            result = -1
            message = "You cannot remove a story that was not written by you"
    else:
        result = -2
        message = "The story you want to delete does not exist"
    res = jsonify({"result": result, "message": message})
    return res



@stories.route('/search_story', methods=["GET"])
def index():
    json_data = request.json()
    search_story = json_data['text']
    if search_story:
        stories = find_story(text=search_story)
        if stories != None:
            return jsonify({"result": 1, "stories": stories})
        else:
            return jsonify({"result": 0})
    else:
        return jsonify({"result": -1})




def find_story(text):
    result = Story.query.filter(func.lower(Story.text).contains(func.lower(text)))
    return result if result.count() > 0 else None


def serializeble_story(story):
    return {'id': story.id,
     'text': story.text,
     'dicenumber': story.dicenumber,
     'date': story.date.strftime("%d/%m/%Y"),
     'like': story.likes,
     'dislike': story.dislikes,
     'author_id': story.author_id}