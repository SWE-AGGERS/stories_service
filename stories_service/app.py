import os
from flakon import create_app
from stories_service.views.stories import api, other_api



_HERE = os.path.dirname(__file__)
_SETTINGS = os.path.join(_HERE, 'settings.ini')


app = create_app(blueprints=[api, other_api],settings=_SETTINGS)
