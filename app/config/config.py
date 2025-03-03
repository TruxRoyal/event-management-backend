import os, secrets
from dotenv import load_dotenv

load_dotenv()

if not os.getenv('SECRET_KEY'):
    raise ValueError('No se ha configurado SECRET_KEY en el archivo .env')

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{os.path.join(BASE_DIR, "events.db")}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_hex(32))
