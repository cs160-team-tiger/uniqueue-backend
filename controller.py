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

    def add_question_to_queue(self, queue_id, student_uuid, question_text, question_attachments=[]):
        pass

    def remove_question_from_queue(self, queue_id, question_id):
        pass

    def check_if_student_currently_in_queue(self, queue_id, student_uuid):
        pass

    def assign_instructor_to_question(self, queue_id, question_id, instructor_uuid):
        pass

    def mark_question_as_solved(self, queue_id, question_id, instructor_uuid):
        pass
