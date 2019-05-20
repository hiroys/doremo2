import sys
import os

FILE_PATH = os.path.dirname(__file__)
PROJECT_NAME = os.path.basename(FILE_PATH)

sys.path.append(os.path.dirname(FILE_PATH))
sys.path.append(FILE_PATH)

from app import app as application

