from flask import Flask


app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/api")
def hello2():
    return "Hello World API!"


@app.route("/appp")
def hello3():
    return "Hello World APPP!"


if __name__ == '__main__':
    print('> entered application api.main')
    app.debug = False
    app.run(host="0.0.0.0")
