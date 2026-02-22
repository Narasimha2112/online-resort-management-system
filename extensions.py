# This file initializes shared extensions like database

from flask_sqlalchemy import SQLAlchemy

# Create SQLAlchemy object without app
db = SQLAlchemy()