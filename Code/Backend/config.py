import os

class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
    JWT_SECRET_KEY = '2394@#$@23424dgf#$%@'
    JWT_ACCESS_TOKEN_EXPIRES = 7200
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'ktrdeveloper@gmail.com'
    MAIL_PASSWORD = 'bxcqdsaekzhnjxps'
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = os.environ.get('CACHE_REDIS_URL') or 'redis://localhost:6379'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379