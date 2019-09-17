import os 
from os.path import join,dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__),'.env')

class DevelopmentConfig:

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{database}?charset=utf8'.format(**{
        'user':os.environ.get("MYSQL_USER")or"root",
        'password':os.environ.get("MYSQL_PASSWORD")or"",
        'host':os.environ.get("DB_HOST")or"localhost",
        'database':os.environ.get("MYSQL_DATABASE")or "test_ems"
    })
    SQLALCHEMY_TRACK_MODIFICATIONS = False #Why? https://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications/33790196#33790196
    SQLALCHEMY_ECHO = False


Config =DevelopmentConfig