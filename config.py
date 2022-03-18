#!/usr/bin/env python

import os 
from dotenv import load_dotenv
load_dotenv()


# Find the absolute file path to the top level project directory
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Base configuration class. Contains default configuration settings + configuration settings applicable to all environments.
    """
    # Default settings
    FLASK_ENV = 'development'
    DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = True

    # Settings applicable to all environments
    SECRET_KEY = os.getenv('SECRET_KEY', default='A very terrible secret key.')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLITE_DATABASE_URI = os.path.join(basedir, 'nci_api.sqlite')
    POSTGRESQL_URI = 'host:port'
    POSTGRESQL_DATABASE_NAME = 'dbname'
    POSTGRESQL_PASSWORD = 'password'

class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    MAIL_SUPPRESS_SEND = True
    SQLITE_DATABASE_URI = os.path.join(basedir, 'test.sqlite')


class ProductionConfig(Config):
    FLASK_ENV = 'production'
    SQLITE_DATABASE_URI = os.getenv('PROD_DATABASE_URl', default=os.path.join(basedir, 'prod.sqlite'))