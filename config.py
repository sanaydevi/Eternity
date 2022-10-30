import os

class Config(object):
    """
    ToDo : Change secret string
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or "secret_string"

    MONGODB_SETTINGS = {'db': 'Eternity'}

    UPLOAD_FOLDER = "uploads"