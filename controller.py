#!/usr/bin/python3
# CS160 FA19 Final Project - UniQueue

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

    def add_question_to_queue(self, queue_id, student_uuid, question_text, question_attachments=[]):
        queue_data = self.ohqueue.fetch_queue_by_qid(queue_id)
        # Check if the queue is open
        if not queue_data["is_open"]:
            return {"error": f"{student_uuid}'s question could not be added to queue {queue_id}: the queue is closed."}
        # Check if student is already in queue
        error_if_student_already_in_queue = self.check_if_student_currently_in_queue(queue_id, student_uuid)
        if isinstance(error_if_student_already_in_queue, dict):
            return error_if_student_already_in_queue
        # Student is not already in queue! Add question.
        new_question_data = self.questions.add_question_data(queue_id=queue_id, asker_uuid=student_uuid, question_text=question_text, question_attachments=question_attachments)
        add_question_id_result = self.ohqueue.add_question_id_to_queue(queue_id, new_question_data["_id"])
        if "error" in add_question_id_result:
            return add_question_id_result
        return queue_data, new_question_data

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
                if question_data["queue_id"] != queue_id:
                    return {"error": f"Question {question_id} has mismatched queue ID: found {question_data['queue_id']} but expected {queue_id}"}
            if "asker_uuid" in question_data:
                if question_data["asker_uuid"] == student_uuid:
                    return {"error": f"Student {student_uuid} is already in queue {queue_id}"}
        return


    # TODO

    def assign_instructor_to_question(self, queue_id, question_id, instructor_uuid):
        pass

    def mark_question_as_solved(self, queue_id, question_id, instructor_uuid):
        pass


def debug():
    controller = Controller()
    print(controller.add_question_to_queue(100, 88, "Test question text"))
    print(controller.add_question_to_queue(100, 88, "Test question text"))
    question_data = controller.add_question_to_queue(100, 94, "Test question text")[1]
    print(controller.ohqueue.fetch_queue_by_qid(100)["question_ids"])
    print(controller.remove_question_from_queue(100, question_data["_id"]))
    print(controller.ohqueue.fetch_queue_by_qid(100)["question_ids"])

# debug()

