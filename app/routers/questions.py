from flask import Blueprint

questions_bp = Blueprint('questions', __name__, url_prefix='/questions')


@questions_bp.route('/', methods=['GET'])
def get_questions():
    return 'получение списка всех вопросов'


@questions_bp.route('/<int:question_id>', methods=['GET'])
def get_question():
    return 'получение одного вопроса '
