#import os
from pathlib import Path

#BASE_PATH = os.path.abspath(os.path.dirname(__file__))

BASE_PATH = Path().absolute()

# email and password for e-mail service
_EMAIL = ''
_PASSWORD = ''


USER_SERVICE_IP = '172.28.1.2'
USER_SERVICE_PORT = '5000'

REACTIONS_SERVICE_IP = '172.28.1.2'
REACTIONS_SERVICE_PORT = '5001'
