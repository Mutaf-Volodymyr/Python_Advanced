from app.models import db


class Response(db.Model):
    __tablename__ = 'response'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    is_agree = db.Column(db.Boolean, nullable=False)
    question_fk = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)


