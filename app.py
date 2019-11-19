#!/usr/bin/python3
# CS160 FA19 Final Project - UniQueue

from flask import Flask, request, jsonify, render_template
# from flask_restful import Resource, Api
from users import Users


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
# api = Api(app)

users = Users()
users.create_user_if_doesnt_exist(88, "David Xiong", "david@berkeley.edu")
users.create_user_if_doesnt_exist(89, "Jiewen Lai", "jiewen@berkeley.edu")
users.create_user_if_doesnt_exist(90, "Zoey Cao", "zoey@berkeley.edu")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users', methods=['GET'])
def get_users():
    uuid = request.args.get('uuid', None)
    email = request.args.get('email', None)
    if uuid:
        return jsonify(users.fetch_user_by_uuid(uuid))
    # If no UUID, attempt to look for email
    if email:
        return jsonify(users.fetch_user_by_email(email))
    # Otherwise, default to returning all users
    return jsonify(users.fetch_all_users())

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
    