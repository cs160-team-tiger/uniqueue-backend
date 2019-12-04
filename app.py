#!/usr/bin/python3
# CS160 FA19 Final Project - UniQueue

from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os

from users import Users
from questions import Questions
from ohqueue import OHQueue
from controller import Controller

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
IMAGE_UPLOAD_FOLDER = "static/question_assets"

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
    users.create_user_if_doesnt_exist(91, "Peng Gu", "peng@berkeley.edu")
    users.create_user_if_doesnt_exist(92, "Sundi Xiao", "zoey@berkeley.edu")
    users.create_user_if_doesnt_exist(93, "James Student", "student@berkeley.edu")
    users.create_user_if_doesnt_exist(94, "Oski Bear", "oski@berkeley.edu")
    users.create_user_if_doesnt_exist(95, "Carol Christ", "carol@berkeley.edu")
    users.create_user_if_doesnt_exist(96, "Peter Peter", "pumpkineater@berkeley.edu")

    ohqueue.add_queue_data(queue_name="David - CS61A", instructor_id=88, location_name="Soda 210", is_open=True, motd="Project 4 due next Tuesday. Ask Miriam if you have questions about homework.", location_latitude=31.231416, location_longitude=-123.125223)
    ohqueue.add_queue_data(queue_name="Jiewen's CS160 OH", instructor_id=89, location_name="Cory 441", is_open=True, motd="All homework questions are welcome. We will not be answering midterm questions.", location_latitude=31.231216, location_longitude=-123.125523)
    ohqueue.add_queue_data(queue_name="CS61B (Peng) Office Hours", instructor_id=91, location_name="Jacobs 220", is_open=True, motd="If you must cry, do it outside.", location_latitude=31.231222, location_longitude=-123.125515)

    controller.add_question_to_queue(queue_id=100, student_uuid=88, question_text="Question A is intriguing")
    controller.add_question_to_queue(queue_id=100, student_uuid=90, question_text="Question B is vexing")
    controller.add_question_to_queue(queue_id=100, student_uuid=92, question_text="Question A is asinine")
    controller.add_question_to_queue(queue_id=100, student_uuid=91, question_text="Question B makes me want to cry")
    controller.add_question_to_queue(queue_id=100, student_uuid=94, question_text="Question C is too difficult for me")
    controller.add_question_to_queue(queue_id=101, student_uuid=88, question_text="Question D is puzzling")
    controller.add_question_to_queue(queue_id=101, student_uuid=89, question_text="Question C is so difficult")
    controller.add_question_to_queue(queue_id=101, student_uuid=92, question_text="Question F is actually pretty easy")
    controller.add_question_to_queue(queue_id=101, student_uuid=90, question_text="Question C is so stumping")
    controller.add_question_to_queue(queue_id=102, student_uuid=89, question_text="Question C is incomprehensible")
    controller.add_question_to_queue(queue_id=102, student_uuid=92, question_text="Question I is okay at best")

    controller.assign_image_to_question(101, "static/question_assets/101_q5screenshot.jpg")
    controller.assign_instructor_to_question(101, 88)
    controller.assign_instructor_to_question(109, 96)
    controller.mark_question_as_resolved(100, 90)
    controller.mark_question_as_helping(104, 95)
    controller.mark_question_as_helping(106, 89)

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

@app.route('/questions/assigninstructor', methods=['POST'])
def assign_instructor_to_question():
    question_id = request.form.get('id', None)
    instructor_uuid = request.form.get('instructor_uuid', None)
    if not question_id or not instructor_uuid:
        question_id = request.args.get('id', None)
        instructor_uuid = request.args.get('instructor_uuid', None)
        if not question_id or not instructor_uuid:
            error_message = {'error': 'Missing or malformed parameters'}
            return jsonify(error_message)
    print("DEBUG: Assigning question 1")
    result = controller.assign_instructor_to_question(question_id=question_id, instructor_uuid=instructor_uuid)
    return jsonify(result)

@app.route('/questions/markhelping', methods=['POST'])
def mark_question_as_helping():
    question_id = request.form.get('id', None)
    instructor_uuid = request.form.get('instructor_uuid', None)
    if not question_id or not instructor_uuid:
        question_id = request.args.get('id', None)
        instructor_uuid = request.args.get('instructor_uuid', None)
        if not question_id or not instructor_uuid:
            error_message = {'error': 'Missing or malformed parameters'}
            return jsonify(error_message)
    result = controller.mark_question_as_helping(question_id=question_id, instructor_uuid=instructor_uuid)
    return jsonify(result)

@app.route('/questions/markresolved', methods=['POST'])
def mark_question_as_resolved():
    question_id = request.form.get('id', None)
    instructor_uuid = request.form.get('instructor_uuid', None)
    if not question_id or not instructor_uuid:
        question_id = request.args.get('id', None)
        instructor_uuid = request.args.get('instructor_uuid', None)
        if not question_id or not instructor_uuid:
            error_message = {'error': 'Missing or malformed parameters'}
            return jsonify(error_message)
    result = controller.mark_question_as_resolved(question_id=question_id, instructor_uuid=instructor_uuid)
    return jsonify(result)

@app.route('/questions/revertstatus', methods=['POST'])
def revert_question_to_incomplete():
    question_id = request.form.get('id', None)
    if not question_id:
        question_id = request.args.get('id', None)
        if not question_id:
            error_message = {'error': 'Missing or malformed parameters'}
            return jsonify(error_message)
    result = controller.revert_question_to_incomplete(question_id=question_id)
    return jsonify(result)

@app.route('/questions/uploadimage', methods=['POST'])
def upload_image_to_question():
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ['jpg', 'jpeg', 'png']
    question_id = request.form.get('id', None)
    if not question_id:
        question_id = request.args.get('id', None)
        if not question_id:
            error_message = {'error': 'Missing or malformed parameter "id"'}
            return jsonify(error_message)
    if 'file' not in request.files:
        error_message = {'error': 'No image file attached'}
        return jsonify(error_message)
    file = request.files['file']
    if file.filename == '':
        error_message = {'error': 'Attached image file cannot have an empty name'}
        return jsonify(error_message)
    if file:
        if not allowed_file(file.filename):
            result = {'error': 'Attached image file must be of type jpg, jpeg, or png'}
        filename = secure_filename(file.filename).strip(' ')
        filepath = os.path.join(IMAGE_UPLOAD_FOLDER, f"{question_id}_{filename}")
        file.save(filepath)
        result = controller.assign_image_to_question(question_id, f"/{filepath}")
    return jsonify(result)

@app.route('/questions/removeimage', methods=['POST'])
def remove_image_from_question():
    question_id = request.form.get('id', None)
    if not question_id:
        question_id = request.args.get('id', None)
        if not question_id:
            error_message = {'error': 'Missing or malformed parameter "id"'}
            return jsonify(error_message)
    result = controller.assign_image_to_question(question_id, None)
    return jsonify(result)

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

@app.route('/queue/offer', methods=['POST'])
def create_question_to_queue():
    _asker_uuid = request.form.get('asker_uuid', None)
    _queue_id = request.form.get('queue_id', None)
    _question_text = request.form.get('question_text', None)
    if not _asker_uuid or not _queue_id or not _question_text:
        _asker_uuid = request.args.get('asker_uuid', None)
        _queue_id = request.args.get('queue_id', None)
        _question_text = request.args.get('question_text', None)
        if not _asker_uuid or not _queue_id or not _question_text:
            error_message = {'error': 'Missing or malformed parameters'}
            return jsonify(error_message)
    result = controller.add_question_to_queue(queue_id=_queue_id, student_uuid=_asker_uuid, question_text=_question_text)
    return jsonify(result)

@app.route('/queue/create', methods=['POST'])
def create_queue_in_db():
    _queue_name = request.form.get('queue_name', None)
    _instructor_id = request.form.get('instructor_id', None)
    _location_name = request.form.get('location_name', None)
    _is_open = request.form.get('is_open', None)
    _motd = request.form.get('motd', None)
    _location_latitude = request.form.get('location_latitude', None)
    _location_longitude = request.form.get('location_longitude', None)
    if not _queue_name or not _instructor_id or not _location_name or not _is_open or not _motd or not _location_latitude or not _location_longitude:
        _queue_name = request.args.get('queue_name', None)
        _instructor_id = request.args.get('instructor_id', None)
        _location_name = request.args.get('location_name', None)
        _is_open = request.args.get('is_open', None)
        _motd = request.args.get('motd', None)
        _location_latitude = request.args.get('location_latitude', None)
        _location_longitude = request.args.get('location_longitude', None)
        if not _queue_name or not _instructor_id or not _location_name or not _is_open or not _motd or not _location_latitude or not _location_longitude:
            error_message = {'error': 'Missing or malformed parameters'}
            return jsonify(error_message)
    result = ohqueue.add_queue_data(_queue_name, _instructor_id, _location_name, _is_open, _motd, _location_latitude, _location_longitude)
    return jsonify(result)

@app.route('/queue/setmotd', methods=['POST'])
def set_queue_motd():
    _queue_id = request.form.get('queue_id', None)
    _motd = request.form.get('motd', None)
    if not _queue_id or not _motd:
        _queue_id = request.args.get('queue_id', None)
        _motd = request.args.get('motd', None)
        if not _queue_id or not _motd:
            error_message = {'error': 'Missing or malformed parameters'}
            return jsonify(error_message)
    result = ohqueue.set_motd(_queue_id, _motd)
    return jsonify(result)

@app.route('/queue/open', methods=['POST'])
def open_queue():
    _queue_id = request.form.get('queue_id', None)
    if not _queue_id:
        _queue_id = request.args.get('queue_id', None)
        if not _queue_id:
            error_message = {'error': 'Missing or malformed parameter "queue_id"'}
            return jsonify(error_message)
    result = ohqueue.open_queue(_queue_id)
    return jsonify(result)

@app.route('/queue/close', methods=['POST'])
def close_queue():
    _queue_id = request.form.get('queue_id', None)
    if not _queue_id:
        _queue_id = request.args.get('queue_id', None)
        if not _queue_id:
            error_message = {'error': 'Missing or malformed parameter "queue_id"'}
            return jsonify(error_message)
    result = ohqueue.close_queue(_queue_id)
    return jsonify(result)

# =========
#   DEBUG
# =========

@app.route('/debug/resetdata', methods=['GET'])
def reset_all_data():
    confirmation = request.args.get('confirm', None)
    if not confirmation:
        return jsonify({'error': 'Must set confirm flag to reset data'})
    users.users_db.purge()
    ohqueue.queue_db.purge()
    questions.question_db.purge()
    add_debug_data()
    return jsonify({'result': 'Successfully reset all data'})

if __name__ == '__main__':
    # add_debug_data()
    app.run(threaded=True, port=5000)
