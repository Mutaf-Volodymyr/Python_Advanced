from flask import Flask

app = Flask(__name__)


@app.route('/')
def hallo_flask():
    return "Hello, Flask!"


@app.route('/user/<name>')
def hallo_name(name):
    return f"Hello, {name}!"


if __name__ == '__main__':
    app.run(debug=True)
