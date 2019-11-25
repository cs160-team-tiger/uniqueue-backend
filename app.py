#!/usr/bin/python3
# CS160 FA19 Final Project - UniQueue

from flask import Flask, request, jsonify, render_template
from users import Users
from questions import Questions
from ohqueue import OHQueue
from controller import Controller

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

users = Users()
questions = Questions()
ohqueue = OHQueue()
controller = Controller()

# =========
#   DEBUG
# =========
def add_debug_data():
    users.create_user_if_doesnt_exist(88, "David Xiong", "david@berkeley.edu")
    users.create_user_if_doesnt_exist(89, "Jiewen Lai", "jiewen@berkeley.edu")
    users.create_user_if_doesnt_exist(90, "Zoey Cao", "zoey@berkeley.edu")

    #questions.add_question_data(queue_id=100, asker_uuid=88, question_text="David's interesting question???")
    #questions.add_question_data(queue_id=100, asker_uuid=90, question_text="Zoey's intriguing question???")
    #questions.add_question_data(queue_id=100, asker_uuid=88, question_text="David's second interesting question???")

    ohqueue.add_queue_data(instructor_id=88, location="Siebel 0220", is_open=True, motd="Do not copy")
    ohqueue.add_queue_data(instructor_id=89, location="Jacobs 320", is_open=True, motd="Don't cry.")

    #(self, queue_id, student_uuid, question_text, question_attachments=[]):
    controller.add_question_to_queue(queue_id=100, student_uuid=88, question_text="Question A")
    controller.add_question_to_queue(queue_id=100, student_uuid=90, question_text="Question B")
    controller.add_question_to_queue(queue_id=101, student_uuid=88, question_text="Question C")
    controller.add_question_to_queue(queue_id=101, student_uuid=89, question_text="Question D")

# Comment out this following line to populate database with test data
# add_debug_data()




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

@app.route('/questions/fetchall', methods=['GET'])
def get_all_questions():
    return jsonify(questions.fetch_all_questions())

@app.route('/questions/fetchallids', methods=['GET'])
def get_all_question_ids():
    return jsonify(questions.fetch_all_question_ids())

@app.route('/questions/fetchbyid', methods=['GET'])
def get_question_by_id():
    _id = request.args.get('id', None)
    if _id:
        return jsonify(questions.fetch_question_by_id(_id))
    else:
        error_message = {'error': 'Missing or malformed parameters'}
        return jsonify(error_message)

# ===========
#   QUEUES
# ===========

@app.route('/queue/peek', methods=['GET'])
def fetch_queue_by_id():
    _id = request.args.get('id', None)
    if _id:
        return jsonify(ohqueue.peek(_id))
    else:
        error_message = {'error': 'Missing or malformed parameters'}
        return jsonify(error_message)

@app.route('/queue/fetchbyid', methods=['GET'])
def peek_queue_by_id():
    _id = request.args.get('id', None)
    if _id:
        return jsonify(ohqueue.fetch_queue_by_qid(_id))
    else:
        error_message = {'error': 'Missing or malformed parameters'}
        return jsonify(error_message)

@app.route('/queue/fetchall', methods=['GET'])
def get_all_queues():
    return jsonify(ohqueue.fetch_all_queues())

@app.route('/queue/offer', methods=['GET'])
def create_question_to_queue():
    _asker_uuid = request.args.get('asker_uuid', None)
    _queue_id = request.args.get('queue_id', None)
    _question_text = request.args.get('question_text', None)

    result = controller.add_question_to_queue(_queue_id, _asker_uuid, _question_text, question_attachments=[])

    if _asker_uuid != None and _queue_id != None and _question_text != None:
        return jsonify(result)
    else:
        error_message = {'error': 'Missing or malformed parameters'}
        return jsonify(error_message)
# =========
#   DEBUG
# =========
def add_debug_data():
    users.create_user_if_doesnt_exist(88, "David Xiong", "david@berkeley.edu")
    users.create_user_if_doesnt_exist(89, "Jiewen Lai", "jiewen@berkeley.edu")
    users.create_user_if_doesnt_exist(90, "Zoey Cao", "zoey@berkeley.edu")

    questions.add_question_data(queue_id=100, asker_uuid=88, question_text="David's interesting question???")
    questions.add_question_data(queue_id=100, asker_uuid=90, question_text="Zoey's intriguing question???")
    questions.add_question_data(queue_id=100, asker_uuid=88, question_text="David's second interesting question???")

    ohqueue.add_queue_data(instructor_id=88, location="Siebel 0220", is_open=True, motd="Do not copy")
    ohqueue.add_queue_data(instructor_id=89, location="Jacobs 320", is_open=True, motd="Don't cry.")
    # ohqueue.add_question_id_to_queue(100, 100)
    # ohqueue.add_question_id_to_queue(100, 101)
    # ohqueue.add_question_id_to_queue(100, 102)

if __name__ == '__main__':
    # add_debug_data()
    app.run(threaded=True, port=5000)
