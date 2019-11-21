#!/usr/bin/python3
# CS160 FA19 Final Project - UniQueue

from flask import Flask, request, jsonify, render_template
from users import Users
from question import Question
import queue

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

users = Users()
users.create_user_if_doesnt_exist(88, "David Xiong", "david@berkeley.edu")
users.create_user_if_doesnt_exist(89, "Jiewen Lai", "jiewen@berkeley.edu")
users.create_user_if_doesnt_exist(90, "Zoey Cao", "zoey@berkeley.edu")

question = Question()
# question.add_question_data(queue_id=100, asker_uuid=88, question_text="David's interesting question???")
# question.add_question_data(queue_id=100, asker_uuid=90, question_text="Zoey's intriguing question???")
# question.add_question_data(queue_id=100, asker_uuid=88, question_text="David's second interesting question???")

queue = queue.Queue()
# queue.add_queue_data(queue_id=100, instructor_id=88, location="Siebel 0220", status=True, motd="Do not copy")
# queue.add_queue_data(queue_id=101, instructor_id=89, location="Jacobs 320", status=True, motd="Don't cry.")
# queue.offer(100, 100)
# queue.offer(100, 101)
# queue.offer(100, 102)

@app.route('/')
def index():
    return render_template('index.html')

# =========
#   USERS
# =========

@app.route('/users/fetchall', methods=['GET'])
def get_all_users():
    return jsonify(users.fetch_all_users())

@app.route('/users/fetchbyuuid', methods=['GET'])
def get_user_by_id():
    uuid = request.args.get('uuid', None)
    if uuid:
        return jsonify(users.fetch_user_by_uuid(uuid))
    else:
        error_message = {'error': 'Missing or malformed parameters'}
        return jsonify(error_message)

@app.route('/users/fetchbyemail', methods=['GET'])
def get_user_by_email():
    email = request.args.get('email', None)
    if email:
        return jsonify(users.fetch_user_by_email(email))
    else:
        error_message = {'error': 'Missing or malformed parameters'}
        return jsonify(error_message)


# =============
#   QUESTIONS
# =============

@app.route('/question/fetchall', methods=['GET'])
def get_all_questions():
    return jsonify(question.fetch_all_questions())

@app.route('/question/fetchallids', methods=['GET'])
def get_all_question_ids():
    return jsonify(question.fetch_all_question_ids())

@app.route('/question/fetchbyid', methods=['GET'])
def get_question_by_id():
    _id = request.args.get('id', None)
    if _id:
        return jsonify(question.fetch_question_by_id(_id))
    else:
        error_message = {'error': 'Missing or malformed parameters'}
        return jsonify(error_message)

# =============
#   QUEUES
# =============

@app.route('/queue/peek', methods=['GET'])
def fetch_queue_by_id():
    _id = request.args.get('id', None)
    if _id:
        return jsonify(queue.peek(_id))
    else:
        error_message = {'error': 'Missing or malformed parameters'}
        return jsonify(error_message)

@app.route('/queue/fetchbyid', methods=['GET'])
def peek_queue_by_id():
    _id = request.args.get('id', None)
    if _id:
        return jsonify(queue.fetch_queue_by_qid(_id))
    else:
        error_message = {'error': 'Missing or malformed parameters'}
        return jsonify(error_message)


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
