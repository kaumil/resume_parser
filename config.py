import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir,'.flaskenv'))


class Config(object):
    LOG_TO_STDOUT = os.environ.get("LOG_TO_STDOUT")

    CACHE_TYPE = "simple"

    CACHE_DEFAULT_TIMEOUT = 300

    ALLOWED_EXTENSIONS = {"docx","pdf"}

    TRAINING_FOLDER = "training"

    TRAINING_CONFIG_JSON = "training_config.json"