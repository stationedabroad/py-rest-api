import os
from flask_sqlalchemy import SQLAlchemy

# Heroku env variable DATABASE_URL (prod use), otherwise local sqlite
db_uri = os.environ.get('DATABASE_URL')
mode = 'prod'
if not db_uri: 
    db_uri = 'sqlite:///appdata.db'
    mode = 'local'

db = SQLAlchemy()