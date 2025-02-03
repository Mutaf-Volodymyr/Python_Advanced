from flask import Flask, jsonify, request
from models import UserModel

users_db: list[UserModel] = []
app = Flask(__name__)

@app.route('/api/v1/user/<name>', methods=["GET"])
def get_user_info(name):
    if not users_db:
        return jsonify({"message": "No users found"})
    for user in users_db:
        if user.name == name:
            return user.model_dump_json(indent=4)
    return jsonify({"message": "No users found"})

@app.route('/api/v1/user', methods=["POST"])
def put_user_info():
    try:
        data = request.get_data(as_text=True)
        user = UserModel.model_validate_json(data)
    except ValueError as e:
        return jsonify({'massage': f'{e}'})
    else:
        users_db.append(user)
        return jsonify({'massage': 'New user added'})




if __name__ == '__main__':
    app.run(debug=True)




