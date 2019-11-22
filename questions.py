#!/usr/bin/python3
# CS160 FA19 Final Project - UniQueue

import tinydb
import utils
import time

class Questions:
	def __init__(self):
		self.question_db = tinydb.TinyDB(f'data/question.json')

	def add_question_data(self, queue_id, asker_uuid, question_text, assigned_uuid=None, answered_uuid=None, question_attachments=[]):
		_id = utils.get_next_available_id('question.json')
		question_dict = {
			'_id': _id,
			'queue_id': queue_id,
			'asker_uuid': asker_uuid,
			'assigned_uuid': assigned_uuid,
			'answered_uuid': answered_uuid,
			'question_text': question_text,
			'question_attachments': question_attachments,
			'creation_time': int(time.time())
		}
		self.question_db.insert(question_dict)
		print(f" > DEBUG: Created question {_id} (Asker UUID: {asker_uuid})")
		return question_dict

	# =========================
	#  Fetch questions by data
	# =========================
	def fetch_question_by_id(self, _id):
		if not isinstance(_id, int):
			_id = int(_id)
		results = self.question_db.search(tinydb.Query()._id == _id)
		if not results:
			return {'error': 'No questions matching the parameters could be found'}
		return results[0]

	def fetch_all_questions(self):
		return self.question_db.all()

	def fetch_all_question_ids(self):
		return sorted([result['_id'] for result in self.question_db.all()])

	# ==================
	#  Update question data
	# ==================

	# TODO: Update this function to be able to edit questions (currently it's just copy pasted from Users.py)
	# def update_user_info(self, uuid, updated_name=None, updated_email=None):
	# 	if updated_name:
	# 		self.users_db.update({'name': name}, tinydb.Query()._uuid == uuid)
	# 	if updated_email:
	# 		self.users_db.update({'email': email}, tinydb.Query()._uuid == uuid)


def debug(keep_changes=True):
	questions = Questions()

	if not keep_changes:
		print(" > WARNING: keep_changes is set to False! Data will be purged!")
	
	# Test adding questions
	questions.add_question_data(queue_id=100, asker_uuid=88, question_text="David's interesting question???")
	questions.add_question_data(queue_id=100, asker_uuid=90, question_text="Zoey's intriguing question???")
		
	# Test fetching questions
	print(question.fetch_all_question_ids())
	print(question.fetch_question_by_id(101))

	if not keep_changes:
		questions.question_db.purge()
		print(" > DEBUG: Purged users database")

# debug(keep_changes=False)
