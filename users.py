#!/usr/bin/python3
# CS160 FA19 Final Project - UniQueue

import tinydb

class Users:
	def __init__(self):
		self.users_db = tinydb.TinyDB(f'data/users.json')

	def add_user_data(self, uuid, name, email, asked_question_ids=[]):
		user_dict = {
			'_uuid': uuid,
			'name': name,
			'email': email,
			'asked_question_ids': asked_question_ids,
			'dummy_key_pls_ignore': []
		}
		self.users_db.insert(user_dict)
		print(f" > DEBUG: Created user {name} (UUID: {uuid})")
		return user_dict

	def create_user_if_doesnt_exist(self, uuid, name, email, asked_question_ids=[]):
		user_result = self.fetch_user_by_uuid(uuid)
		if "error" in user_result and user_result["error"] == "No users matching the parameters could be found":
			self.add_user_data(uuid, name, email, asked_question_ids)	
		if user_result:
			return user_result
		return {"Error": f"Could not create user {uuid} due to an unknown error"}

	# =====================
	#  Fetch users by data
	# =====================
	def fetch_user_by_uuid(self, uuid):
		if not isinstance(uuid, int):
			uuid = int(uuid)
		results = self.users_db.search(tinydb.Query()._uuid == uuid)
		if not results:
			return {'error': 'No users matching the parameters could be found'}
		return results

	def fetch_user_by_name(self, name):
		results = self.users_db.search(tinydb.Query().name == name)
		if not results:
			return {'error': 'No users matching the parameters could be found'}
		return results

	def fetch_user_by_email(self, email):
		results = self.users_db.search(tinydb.Query().email == email)
		if not results:
			return {'error': 'No users matching the parameters could be found'}
		return results

	def fetch_all_users(self):
		return self.users_db.all()

	# ==================
	#  Update user data
	# ==================

	def update_user_info(self, uuid, updated_name=None, updated_email=None):
		if updated_name:
			self.users_db.update({'name': name}, tinydb.Query()._uuid == uuid)
		if updated_email:
			self.users_db.update({'email': email}, tinydb.Query()._uuid == uuid)


def debug(keep_changes=True):
	users = Users()
	
	if not keep_changes:
		print(" > WARNING: keep_changes is set to False! Data will be purged!")
	
	# Test adding students
	users.create_user_if_doesnt_exist(91, "David Xiong", "david@berkeley.edu")
	users.create_user_if_doesnt_exist(92, "Peng Gu", "peng@berkeley.edu")

	# Test fetching students
	print(users.fetch_user_by_uuid(91))
	print(users.fetch_user_by_name('David Xiong'))
	print(users.fetch_user_by_email('david@berkeley.edu'))

	if not keep_changes:
		users.users_db.purge()
		print(" > DEBUG: Purged users database")

