from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

from app.models.responses import Response
from app.models.questions import Question
