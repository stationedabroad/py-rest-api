import os
from flask_sqlalchemy import SQLAlchemy

# Heroku env variable DATABASE_URL (prod use), otherwise local sqlite
db_uri = os.environ.get('DATABASE_URL', 'sqlite:///appdata.db')

db = SQLAlchemy()