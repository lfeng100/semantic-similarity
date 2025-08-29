import os

class Config:
    ENV = os.getenv("APP_ENV", "development")
    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"
    TESTING = False
    JSON_SORT_KEYS = False # default is True
