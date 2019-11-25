#import os
from pathlib import Path

#BASE_PATH = os.path.abspath(os.path.dirname(__file__))

BASE_PATH = Path().absolute()

# email and password for e-mail service
_EMAIL = ''
_PASSWORD = ''

TIMEOUT_DB = 10
TIMEOUT_SERVICES = 5


STORIES_SERVICE_IP = '0.0.0.0'
STORIES_SERVICE_PORT = '5001'

USERS_SERVICE_IP = '0.0.0.0'
USERS_SERVICE_PORT = '5002'

DICE_SERVICE_IP = '0.0.0.0'
DICE_SERVICE_PORT = '5003'

PROFILING_SERVICE_IP = '0.0.0.0'
PROFILING_SERVICE_PORT = '5004'

REACTIONS_SERVICE_IP = '0.0.0.0'
REACTIONS_SERVICE_PORT = '5005'
