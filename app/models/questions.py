from app.models import db


class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String, nullable=False)
    responses = db.relationship('Response', backref='question', lazy='joined', uselist=True)

    def __repr__(self):
        return '<Question %r>' % self.text

class Statistic(db.Model):
    __tablename__ = 'statistic'
    question_fk = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    agree_count = db.Column(db.Integer, nullable=False, default=0)
    disagree_count = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return '<Statistic for Question %r: %r agree, %r disagree>' % (
        self.question_id, self.agree_count, self.disagree_count)
