from flask import Flask
from .database import init_db
from .config import Config
from .models import models #call models through __init__.py
from flask_bootstrap import Bootstrap
import os

def create_app():
    app = Flask(__name__)
    bootstrap = Bootstrap(app)
    app.secret_key = os.urandom(24)
    app.config.from_object(Config) 
    app.app_context().push()
    init_db(app)
    return app

app = create_app()