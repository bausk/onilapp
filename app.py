from flask import Flask
import redis
from scripts.startup import startup_development


app = Flask(__name__)


@app.route("/")
def hello():
    try:
        client = redis.StrictRedis(host='redis-14910.c9.us-east-1-4.ec2.cloud.redislabs.com', port=14910, db=0, password='dis7location')
        res1 = client.set('foo', 'bar')
        res2 = client.get('foo')
    except Exception as e:
        print(e)
    return "Hello World! {}, {}".format(res1, res2)

if __name__ == '__main__':
    startup_development()

    print('> entered application app.main')
    app.debug = False
    app.run(host="0.0.0.0")
