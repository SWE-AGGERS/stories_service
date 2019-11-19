from flask import Blueprint, request, redirect, render_template, abort, json, jsonify
from sqlalchemy import func
from flask import Blueprint, redirect, render_template, request
from flask_login import (current_user, login_user, logout_user,login_required)
from stories_service.database import db, Story
from stories_service.views.check_stories import check_storyV2, InvalidStory, TooLongStoryError, TooSmallStoryError, WrongFormatDiceError, WrongFormatSingleDiceError, WrongFormatStoryError
from flakon import SwaggerBlueprint, JsonBlueprint, create_app
import requests

other_api = JsonBlueprint('api', __name__)

@other_api.route('/')
def some():
    return {'here': 1}



api = SwaggerBlueprint('Swagger API', 'swagger' ,swagger_spec='openapi.yaml')





# Method requested by the microservice reactions_service to
# check if a story exists via its story id.








@api.operation('/story_exists/<storyid>')
def story_exists(storyid):
    q = db.session.query(Story).filter_by(id=storyid)
    story = q.first()
    if story is not None:
        result = jsonify({"result": 1})
        return result
    else:
        abort(404)




@api.operation('/story_list/<userid>')
def story_exists(userid):
    stories = db.session.query(Story).filter(Story.author_id == userid)
    if stories is not None:
        result = jsonify({"stories": stories})
        return result
    else:
        abort(404)









@api.operation('/stories', methods=['POST', 'GET'])
def stories():
    if 'POST' == request.method:

        # Verify that the user exists

        code = -1
        message = ""




        r = requests.get('/user_exists/'+current_user.id)

        json_data = r.json()
        user = json_data['result']
        if user == -1:

            # if it does not exist I set the params accordingly

            code = -1
            message = "The user does not exists"
            result = jsonify({"result": code, "message": message, "stories": []})
            return result
        else:

            # otherwise I create the story and I verify that it is valid


            # Create a new story
            new_story = Story()
            new_story.author_id = current_user.id
            new_story.likes = 0
            new_story.dislikes = 0



            # request of story and faces

            r = requests.get('/dice')

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
                code = -2
                message = "There was an error. Try again."

            except WrongFormatDiceError:
                # print('ERROR 2', file=sys.stderr)
                code = -3
                message = "There was an error. Try again."

            except WrongFormatSingleDiceError:
                # print('ERROR 5', file=sys.stderr)
                code = -4
                message = "There was an error. Try again."

            except TooLongStoryError:
                # print('ERROR 3', file=sys.stderr)
                code = -5
                message = "The story is too long. The length is > 1000 characters."

            except TooSmallStoryError:
                # print('ERROR 4', file=sys.stderr)
                code = -6
                message = "The number of words of the story must greater or equal of the number of resulted faces."



            except InvalidStory:
                # print('ERROR 6', file=sys.stderr)
                code = -7
                message = "Invalid story. Try again!"




        allstories = db.session.query.all()
        result = jsonify({"result": code, "message": message, "stories": allstories})
        return result





    elif 'GET' == request.method:
        allstories = db.session.query.all()
        if allstories is not None:
            result = jsonify({"stories": allstories})
            return result
        else:
            abort(404)






@api.operation('/stories/<storyid>', methods=['GET'])
def get_story_detail(storyid):
    q = db.session.query(Story).filter_by(id=storyid)
    story = q.first()
    if story is not None:
        result = jsonify({"story": story})
        return result
    else:
        abort(404)



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


@api.operation('/stories/random', methods=['GET'])
def random_story():
    q = db.session.query(Story).order_by(func.random()).limit(1)
    random_story_from_db = q.first()
    if random_story_from_db is not None:
        result = jsonify({"story": random_story_from_db})
        return result
    else:
        abort(404)



@api.operation('/stories/filter', methods=['POST'])
def filter_stories():
    if request.method == 'POST':


        r = requests.get("/dates_filter_stories")

        json_data = r.json()
        init_date = json_data['init_date']
        end_date = json_data['end_date']

        if init_date > end_date:
            result = jsonify({"result": -1})
            return result


        f_stories = db.session.query(Story)\
            .filter(Story.date >= init_date)\
            .filter(Story.date <= end_date)\
            .all()


        if f_stories is not None:
            result = jsonify({'result': 0,"stories": f_stories})
            return result
        else:
            abort(404)








@api.operation('/stories/remove/<storyid>', methods=['POST'])
def get_remove_story(storyid):

    message = ""
    result = -1


    # Remove story
    q = db.session.query(Story).filter_by(id=storyid)
    story = q.first()
    if story is not None:
        if story.author_id == current_user.id:
            r = requests.get("/user_exists"+current_user.id)
            json_data = r.json()
            code = json_data['result']
            if code:
                db.session.delete(story)
                db.session.commit()
                result = 1
                message = "Story removed"
            else:
                result = -1
                message = "There was a problem with the removal of the story. In particular in the deletion of the reactions"
        else:
            result = -2
            message = "You cannot remove a story that was not written by you"
    else:
        result = -3
        message = "The story you want to delete does not exist"
    res = jsonify({"result": result, "message": message})
    return res



@api.operation('/search_story', methods=["GET"])
def index():
    json_data = request.json()
    search_story = json_data['text']
    if search_story:
        stories = find_story(text=search_story)
        if stories != None:
            res = jsonify({"stories": stories})
            return res
        else:
            abort(404)
    else:
        abort(404)




def find_story(text):
    result = Story.query.filter(func.lower(Story.text).contains(func.lower(text)))
    return result if result.count() > 0 else None