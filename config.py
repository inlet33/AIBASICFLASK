#
import os 
from os.path import join,dirname
#from dotenv import load_dotenv

class DevelopmentConfig:

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymsql://root: @localhost/test_ems?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


Config =DevelopmentConfig