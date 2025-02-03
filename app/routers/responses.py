from flask import Blueprint

responses_bp = Blueprint('responses', __name__, url_prefix='/responses')


@responses_bp.route('/<int:question_id>', methods=['POST'])
def add_response():
    return 'добавления ответа на вопрос'