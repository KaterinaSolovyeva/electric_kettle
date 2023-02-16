import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')

    KETTLE_POWER = 2.2
    BASE_TEMPERATURE = 22
    MAX_WATER_QUANTITY = 1.7
    SHUTDOWN_TEMPERATURE = 100
    BOILING_TIME = 10


LOGGING_CONFIG = {
    'version': 1,
    'root': {
        "handlers": ['default', 'file'],
        "level": 'INFO'
    },
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] - %(message)s',
            'datefmt': '%d/%m/%Y %H:%M:%S',
        },
    },
    'handlers': {
        'default': {
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'standard',
            'filename': 'kettle.log',
        }
    },
}
