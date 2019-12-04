#!/usr/bin/python3
# CS160 FA19 Final Project - UniQueue

import tinydb
import utils
import time
from users import Users

class Questions:
	def __init__(self):
		self.users = Users()
		self.question_db = tinydb.TinyDB(f'data/question.json')

	def add_question_data(self, queue_id, asker_uuid, question_text, status="incomplete", assigned_uuid=None, answered_uuid=None, question_attachments=None):
		_id = utils.get_next_available_id('question.json')
		question_dict = {
			'_id': _id,
			'queue_id': queue_id,
			'asker_uuid': asker_uuid,
			'asker_name': self.users.fetch_user_by_uuid(asker_uuid)['name'],
			'assigned_uuid': assigned_uuid,
			'assigned_name': self.users.fetch_user_by_uuid(assigned_uuid)['name'] if assigned_uuid else None,
			'answered_uuid': answered_uuid,
			'answered_name': self.users.fetch_user_by_uuid(answered_uuid)['name'] if answered_uuid else None,
			'question_text': question_text,
			'question_attachments': question_attachments,
			'creation_time': int(time.time()),
			'status': status
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
		results = self.question_db.get(tinydb.Query()._id == _id)
		if not results:
			return {'error': f'No questions matching ID {_id} could be found'}
		return results

	def fetch_all_questions(self):
		return self.question_db.all()

	def fetch_all_question_ids(self):
		return sorted([result['_id'] for result in self.question_db.all()])

	# ==================
	#  Update question data
	# ==================

	def change_question_status(self, _id, status):
		if status not in ['incomplete', 'assigned', 'helping', 'resolved']:
			return {'error': f'{status} is not a valid status. Must be: incomplete, assigned, helping, or resolved.'}
		_id = int(_id)
		question_data = self.fetch_question_by_id(_id)
		if "error" in question_data:
			return {'error': f'No questions matching ID {_id} could be found; question status not changed'}
		self.question_db.update({'status': status}, tinydb.Query()._id == _id)


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
