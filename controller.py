#!/usr/bin/python3
# CS160 FA19 Final Project - UniQueue

import tinydb
from users import Users
from questions import Questions
from ohqueue import OHQueue

# Note: For now we're just deleting questions that have been marked as "solved". Perhaps we'll find a place for them someday.

class Controller():
    def __init__(self):
        self.users = Users()
        self.questions = Questions()
        self.ohqueue = OHQueue()

    # =======================
    #   Question Management
    # =======================

    def add_question_to_queue(self, queue_id, student_uuid, question_text, status="incomplete", question_attachments=None):
        queue_id = int(queue_id)
        student_uuid = int(student_uuid)
        queue_data = self.ohqueue.fetch_queue_by_qid(queue_id)
        # check if the ID is valid
        if "error" in queue_data or queue_data == None:
            return {"msg": f"{queue_id} is an invalid queue ID!", 'status':False}
        # Check if the queue is open
        if not queue_data["is_open"]:
            return {"msg": f"{student_uuid}'s question could not be added to queue {queue_id}: the queue is closed.", 'status':False}
        # Check if student is already in queue
        error_if_student_already_in_queue = self.check_if_student_currently_in_queue(queue_id, student_uuid)
        if isinstance(error_if_student_already_in_queue, dict):
            if "error" not in error_if_student_already_in_queue:
                return {"msg": f"Student {student_uuid} is already in queue {queue_id}!", 'status':False}
            return {'msg': error_if_student_already_in_queue, 'status': False}
        # Student is not already in queue! Add question.
        new_question_data = self.questions.add_question_data(queue_id=queue_id, asker_uuid=student_uuid, question_text=question_text, status=status, question_attachments=question_attachments)
        add_question_id_result = self.ohqueue.add_question_id_to_queue(queue_id, new_question_data["_id"])
        if "error" in add_question_id_result:
            return {'msg': add_question_id_result, 'status':False}
        retval = {'queue':add_question_id_result, 'question':new_question_data, 'status': True}
        return retval

    def remove_question_from_queue(self, queue_id, question_id):
        queue_data = self.ohqueue.fetch_queue_by_qid(queue_id)
        if "error" in queue_data:
            return {"error": f"Queue {queue_id} does not exist. Are you sure the queue ID is correct?"}
        remove_question_id_result = self.ohqueue.remove_question_id_from_queue(queue_id, question_id)
        if "error" in remove_question_id_result:
            return remove_question_id_result
        return queue_data

    def check_if_student_currently_in_queue(self, queue_id, student_uuid):
        # This function is a bit weird - it checks if a student is currently in a queue,
        # but returns a dictionary containing an error if they are and returns None if they are
        # not. As such, in order to check if a student is not in the queue, you must use:
        #    if self.check_if_student_currently_in_queue(qID, sID) == None:
        # or if not self.check_if_student_currently_in_queue(qID, sID):
        # Checking for `true` will check if an error was found.
        # This is due to how errors are handled in the backend. Sorry.
        queue_data = self.ohqueue.fetch_queue_by_qid(queue_id)
        if "error" in queue_data:
            return {"error": f"Queue {queue_id} does not exist. Are you sure the queue ID is correct?"}
        for question_id in queue_data['question_ids']:
            question_data = self.questions.fetch_question_by_id(question_id)
            if "error" in question_data:
                return {"error:": f"Question {question_id} returned error: {question_data['error']}"}
            if "queue_id" in question_data:
                if int(question_data["queue_id"]) != int(queue_id):
                    return {"error": f"Question {question_id} has mismatched queue ID: found {question_data['queue_id']} but expected {queue_id}"}
            if "asker_uuid" in question_data:
                if question_data["asker_uuid"] == student_uuid:
                    #return {"error": f"Student {student_uuid} is already in queue {queue_id}"}
                    # Return the question that the student asked
                    return question_data
        return None

    def assign_instructor_to_question(self, question_id, instructor_uuid):
        # Check if the question is eligible for assigning to an instructor (incomplete or assigned).
        question_id = int(question_id)
        question_data = self.questions.fetch_question_by_id(question_id)
        if 'error' in question_data:
            return {'error': f'No questions matching ID {question_id} could be found. Instructor not assigned'}
        if question_data['status'] not in ['incomplete', 'assigned']:
            return {'error': f'Question {question_id} cannot be assigned to another instructor: current status is {question_data["status"]}'}

        # We're good! Change the status of the question and assign the instructor
        self.questions.change_question_status(question_id, status="assigned")
        self.questions.question_db.update({"assigned_uuid": instructor_uuid}, tinydb.Query()._id == question_id)
        self.questions.question_db.update({"assigned_name": self.users.fetch_user_by_uuid(instructor_uuid)[0]['name']}, tinydb.Query()._id == question_id)
        print(f" > DEBUG: Assigning question {question_id} to instructor {instructor_uuid}")
        return self.questions.fetch_question_by_id(question_id)

    def mark_question_as_helping(self, question_id, instructor_uuid):
        # If there isn't an assigned instructor, assign current one
        question_id = int(question_id)
        question_data = self.questions.fetch_question_by_id(question_id)
        if 'error' in question_data:
            return {'error': f'No questions matching ID {question_id} could be found. Could not mark as helping.'}
        if not question_data['assigned_uuid']:
            self.assign_instructor_to_question(question_id, instructor_uuid)
        # Now mark the question status as helping.
        self.questions.change_question_status(question_id, status="helping")
        print(f" > DEBUG: Marking question {question_id} as 'helping' (instructor: {instructor_uuid})")
        return self.questions.fetch_question_by_id(question_id) 

    def mark_question_as_resolved(self, question_id, instructor_uuid):
        # If there isn't an assigned instructor, assign one.
        question_id = int(question_id)
        question_data = self.questions.fetch_question_by_id(question_id)
        if 'error' in question_data:
            return {'error': f'No questions matching ID {question_id} could be found. Could not mark as helping.'}
        # If there's no UUID currently assigned, take the credit. If there is one, leave it as is
        if not question_data['assigned_uuid']:
            self.assign_instructor_to_question(question_id, instructor_uuid)
        # Now mark the question status as resolved.
        self.questions.question_db.update({"answered_uuid": instructor_uuid}, tinydb.Query()._id == question_id)
        self.questions.question_db.update({"answered_name": self.users.fetch_user_by_uuid(instructor_uuid)[0]['name']}, tinydb.Query()._id == question_id)
        change_status_result = self.questions.change_question_status(question_id, status="resolved")
        print(f" > DEBUG: Marking question {question_id} as 'resolved' (instructor: {instructor_uuid})")
        return self.questions.fetch_question_by_id(question_id) 

    def revert_question_to_incomplete(self, question_id):
        question_id = int(question_id)
        question_data = self.questions.fetch_question_by_id(question_id)
        if 'error' in question_data:
            return {'error': f'No questions matching ID {question_id} could be found. Could not mark as helping.'}
        if question_data['assigned_uuid']:
            self.questions.question_db.update({"assigned_uuid": None}, tinydb.Query()._id == question_id)
            self.questions.question_db.update({"assigned_name": None}, tinydb.Query()._id == question_id)
        if question_data['answered_uuid']:
            self.questions.question_db.update({"answered_uuid": None}, tinydb.Query()._id == question_id)
            self.questions.question_db.update({"answered_name": None}, tinydb.Query()._id == question_id)
        self.questions.change_question_status(question_id, status="incomplete")
        print(f" > DEBUG: Reverting question {question_id} to 'incomplete'")
        return self.questions.fetch_question_by_id(question_id) 

    def assign_image_to_question(self, question_id, image_filepath):
        question_id = int(question_id)
        question_data = self.questions.fetch_question_by_id(question_id)
        if 'error' in question_data:
            return {'error': f'No questions matching ID {question_id} could be found. Could not mark as helping.'}
        self.questions.question_db.update({"question_attachments": image_filepath}, tinydb.Query()._id == question_id)
        print(f" > DEBUG: Assigned image {image_filepath} to {question_id}")
        return self.questions.fetch_question_by_id(question_id) 


