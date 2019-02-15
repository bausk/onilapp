# app.py

from flask import Flask
app = Flask(__name__)
import redis


@app.route("/")
def hello():
    client = redis.Redis(host='aws-my-ykaw4bq1mf7j.pw70f5.0001.use1.cache.amazonaws.com')
    res1 = client.set('foo', 'bar')
    res2 = client.get('foo')
    return "Hello World! {}, {}".format(res1, res2)
