from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from app.config.config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CORS(app)
    
    from app.routes.api import register_api
    register_api(app)
    
    return app