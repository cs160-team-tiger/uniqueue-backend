#!/usr/bin/python3
# CS160 FA19 Final Project - UniQueue

import tinydb

def get_next_available_id(db_file):
	db = tinydb.TinyDB(f'data/{db_file}')
	if db_file == "users.json":
		# TODO: Replace this with Google Accounts' UUID solution. 
		# For now, just assign numbers sequentially
		search_results = db.search(tinydb.where('_uuid'))
		if not search_results:
			# Start at ID = 100 for completely arbitrary reasons
			return 100
		max_uuid = max(search_results, key=lambda result: result['_uuid'])['_uuid']
		return max_uuid + 1
	# Otherwise, increment ID sequentially.
	search_results = db.search(tinydb.where('_id'))
	if not search_results:
		# Start at ID = 100 for completely arbitrary reasons (mostly debugging)
		return 100
	max_id = max(search_results, key=lambda result: result['_id'])['_id']
	return max_id + 1

def debug():
	print(get_next_available_id("users.json"))
