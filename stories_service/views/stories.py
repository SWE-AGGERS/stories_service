from flask import jsonify
import json
from sqlalchemy import func
from flask import Blueprint, request
from stories_service.database import db, Story
from stories_service.views.check_stories import check_storyV2, InvalidStory, TooLongStoryError, TooSmallStoryError, WrongFormatDiceError, WrongFormatSingleDiceError, WrongFormatSingleFaceError, WrongFormatStoryError
import requests
from requests.exceptions import Timeout
import sys
from stories_service.constants import USER_SERVICE_IP, USER_SERVICE_PORT, REACTIONS_SERVICE_IP, REACTIONS_SERVICE_PORT

stories_blueprint = Blueprint('stories_blueprint', __name__)

TIMEOUT = 5


@stories_blueprint.route('/story_exists/<storyid>')
def story_exists(storyid):
    q = db.session.query(Story).filter_by(id=storyid)
    story = q.first()
    if story is not None:
        result = jsonify({"result": 1})
    else:
        result = jsonify({"result": 0})
    return result




@stories_blueprint.route('/story_list/<userid>')
def story_list(userid):




    ris = send_request_user_service(userid)

    if ris == -2:
        message = "Timeout: the user service is not responding"
        result = jsonify({"result": -2, "message": message})
        return result

    elif ris != -1:


        allstories = db.session.query(Story).filter(Story.author_id == int(userid)).all()




        if len(allstories) > 0:

            arr = []


            ris = send_request_reactions_service(arr,allstories)

            if ris == -2:
                message = "One or more of the stories written by the user does not exists in the reaction database"
                result = jsonify({"result": -3, "message": message})
            elif ris == -1:
                message = "Timeout: the reactions service is not responding"
                result = jsonify({"result": -4, "message": message})
            else:
                message = "Here are the stories written by the user"
                result = jsonify({"result": 1, "stories": arr, 'message': message})
            return result
        else:
            message = "No story has been found"
            result = jsonify({"result": 0, 'message': message})
            return result
    else:
        message = "The user does not exists"
        result = jsonify({"result": -1, 'message': message})
        return result









@stories_blueprint.route('/stories', methods=['POST', 'GET'])
def get_stories():
    if 'POST' == request.method:

        # Verify that the user exists

        code = -1
        message = ""

        arr = []

        allstories = db.session.query(Story).all()



        ris = send_request_reactions_service(arr=arr,allstories=allstories)


        if ris == -2:
            message = "One or more of the stories written by the user does not exists in the reaction database"
            result = jsonify({"result": -10, "message": message})
            return result
        elif ris == -1:
            message = "Timeout: the reactions service is not responding"
            result = jsonify({"result": -11, "message": message})
            return result
        else:

            userid = request.args.get('userid')

            if userid == None:
                message = "The userid is None"
                result = jsonify({"result": -9, "message": message,  "stories": arr})
                return result

            ris = send_request_user_service(userid)

            if ris == -2:
                message = "Timeout: the user service is not responding"
                result = jsonify({"result": -7, "message": message})
                return result

            elif ris == -1:

                # if it does not exist I set the params accordingly

                code = 0
                message = "The user does not exists"
                result = jsonify({"result": code, "message": message,  "stories": arr})
                return result
            else:

                # otherwise I create the story and I verify that it is valid


                # Create a new story
                new_story = Story()
                new_story.author_id = userid
                new_story.likes = 0
                new_story.dislikes = 0


                if request.json == None:
                    message = "Wrong parameters"
                    result = jsonify({"result": -8, "message": message, "stories": arr})
                    return result

                created_story = request.json['created_story']

                if len(created_story) != 2:
                    message = "Wrong parameters"
                    result = jsonify({"result": -8, "message": message, "stories": arr})
                    return result

                try:
                    text = created_story['text']
                    roll = created_story['roll']
                except KeyError:
                    message = "Wrong parameters"
                    result = jsonify({"result": -8, "message": message, "stories": arr})
                    return result


                if text == None or roll == None:
                    message = "Wrong parameters"
                    result = jsonify({"result": -8, "message": message, "stories": arr})
                    return result



                if (type(roll) is str):
                    roll = roll.replace("[", "")
                    roll = roll.replace("]", "")
                    roll = roll.replace("'", "")
                    roll = roll.replace(" ", "")
                    aux = roll.split(",")
                    roll = aux

                if not isinstance(roll, list):
                    message = "There was an error. Try again."
                    result = jsonify({"result": -2, "message": message, "stories": arr})
                    return result

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
                    arr.append(serializeble_story(new_story))
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




            result = jsonify({"result": code, "message": message,  "stories": arr})
            return result





    elif 'GET' == request.method:

        allstories = db.session.query(Story).all()

        if len(allstories) > 0:

            arr = []
            ris = send_request_reactions_service(arr,allstories)

            if ris == -2:
                message = "One or more of the stories written by the user does not exists in the reaction database"
                result = jsonify({"result": -1, "message": message})
                return result
            elif ris == -1:
                message = "Timeout: the reactions service is not responding"
                result = jsonify({"result": -2, "message": message})
                return result
            else:
                message = "Stories"
                return jsonify({"result": 1, "stories": arr, 'message': message})
        else:
            message = "No stories"
            return jsonify({"result": 0, 'message': message})





@stories_blueprint.route('/stories/<storyid>', methods=['GET'])
def get_story_detail(storyid):
    q = db.session.query(Story).filter_by(id=storyid)
    story = q.first()



    if story != None:

        arr = []
        allstories = []
        allstories.append(story)

        ris = send_request_reactions_service(arr, allstories)

        if ris == -2:
            message = "The story does not exists in the reaction database"
            result = jsonify({"result": -1, "message": message})
        elif ris == -1:
            message = "Timeout: the reactions service is not responding"
            result = jsonify({"result": -2, "message": message})
        else:
            message = "The story exists"
            result = json.dumps({"result": 1, "message": message, "story": arr[0]})
        return result
    else:
        message = "The story does not exists"
        result = json.dumps({"result": 0, "message": message})
        return result



@stories_blueprint.route('/stories/random', methods=['GET'])
def random_story():
    q = db.session.query(Story).order_by(func.random()).limit(1)
    random_story_from_db = q.first()


    if random_story_from_db != None:

        arr = []
        allstories = []
        allstories.append(random_story_from_db)

        ris = send_request_reactions_service(arr, allstories)

        if ris == -2:
            message = "The story does not exists in the reaction database"
            result = jsonify({"result": -1, "message": message})
        elif ris == -1:
            message = "Timeout: the reactions service is not responding"
            result = jsonify({"result": -2, "message": message})
        else:
            message = "The story exists"
            result = json.dumps({"result": 1, "message": message, "story": arr[0]})
        return result
    else:
        message = "The story does not exists"
        result = json.dumps({"result": 0, "message": message})
        return result





@stories_blueprint.route('/stories/filter', methods=['POST'])
def filter_stories():
    if request.method == 'POST':

        message = "Missing params"
        result = jsonify({"result": -2, "message": message})



        if request.json == None:
            return result

        if len(request.json) != 1:
            return result

        try:
            info = request.json['info']
            init_date = info['init_date']
            end_date = info['end_date']
            userid = info['userid']

        except KeyError:
            return result



        ris = send_request_user_service(userid)

        if ris == -2:
            message = "Timeout: the user service is not responding"
            result = jsonify({"result": -4, "message": message})
            return result


        elif ris == -1:


            message = "The user does not exists"
            result = jsonify({"result": -5, "message": message})
            return result

        else:


            if init_date > end_date:
                message = "The init date is greater than the end date"
                result = jsonify({"result": -1, "message" : message})
                return result


            f_stories = db.session.query(Story)\
                .filter(Story.date >= init_date)\
                .filter(Story.date <= end_date)\
                .all()



            if len(f_stories) != 0:


                arr = []


                ris = send_request_reactions_service(arr, f_stories)

                if ris == -2:
                    message = "One or more of the stories written by the user does not exists in the reaction database"
                    result = jsonify({"result": -6, "message": message})
                elif ris == -1:
                    message = "Timeout: the reactions service is not responding"
                    result = jsonify({"result": -7, "message": message})
                else:
                    message = "At least one story has been found"
                    result = jsonify({"result": 1, "stories": arr, "message": message})
                return result
            else:
                message = "No story has been found"
                result = jsonify({"result": 0, "message": message})
                return result









@stories_blueprint.route('/stories/remove/<storyid>', methods=['POST'])
def remove_story(storyid):

    message = ""
    result = -1

    userid = request.args.get('userid')

    if userid == None:
        message = "userid not inserted"
        result = jsonify({"result": -2, "message": message})
        return result

    ris = send_request_user_service(userid)

    if ris == -2:
        message = "Timeout: the user service is not responding"
        result = jsonify({"result": -3, "message": message})
        return result


    elif ris == -1:

        # if it does not exist I set the params accordingly

        message = "The user does not exists"
        result = jsonify({"result": -4, "message": message})
        return result

    else:



        # Remove story
        q = db.session.query(Story).filter_by(id=storyid)
        story = q.first()
        if story is not None:
            if int(story.author_id) == int(userid):
                db.session.delete(story)
                db.session.commit()
                result = 1
                message = "Story removed"
            else:
                result = 0
                message = "You cannot remove a story that was not written by you"
        else:
            result = -1
            message = "The story you want to delete does not exist"
        res = jsonify({"result": result, "message": message})
        return res



@stories_blueprint.route('/search_story', methods=["GET"])
def index():


    message = "Story empty"
    result = jsonify({"result": -2, 'message': message})


    if request.json == None:
        return result

    if len(request.json) != 1:
        return  result

    try:
        story = request.json['story']
        search_story = story['text']

    except KeyError:
        return result


    if search_story == None:
        message = "Story empty"
        result = jsonify({"result": -2, 'message': message})
        return result


    if search_story != ' ' and search_story != '':


        allstories = find_story(text=search_story)

        if allstories != None:

            arr = []

            ris = send_request_reactions_service(arr, allstories)

            if ris == -2:
                message = "One or more of the stories does not exists in the reaction database"
                result = jsonify({"result": -3, "message": message})
            elif ris == -1:
                message = "Timeout: the reactions service is not responding"
                result = jsonify({"result": -4, "message": message})
            else:
                message = "At least one story has been found"
                result = jsonify({"result": 1, "stories": arr, "message": message})
            return result
        else:
            message = "No story has been found"
            result = jsonify({"result": 0, "message": message})
            return result
    else:
        message = "The text inserted is empty"
        return jsonify({"result": -1, 'message': message})




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






def send_request_reactions_service(arr,allstories):


    if allstories is not None:



        for elem in allstories:

            url = 'http://' + REACTIONS_SERVICE_IP + ':' + REACTIONS_SERVICE_PORT + '/reactions/' + str(elem.id)

            try:
                r = requests.get(url, timeout=TIMEOUT)
            except Timeout:
                return -1

            json_data = r.json()
            story_id = json_data['story_id']
            if story_id != -1:
                like = json_data['like']
                dislike = json_data['dislikes']

                elem.like = like
                elem.dislikes = dislike
                arr.append(serializeble_story(elem))
            else:
                return -2
        return 1
    else:
        return 0


def send_request_user_service(userid):

    url = 'http://' + USER_SERVICE_IP + ':' + USER_SERVICE_PORT + '/user_exists/' + userid

    try:
        r = requests.get(url, timeout=TIMEOUT)
    except Timeout:
        return -2

    json_data = r.json()
    return json_data['response']


