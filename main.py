#!/usr/bin/python3

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1> UniQueue Backend Test 🎉 </h1>'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')