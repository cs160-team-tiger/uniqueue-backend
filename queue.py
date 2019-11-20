import tinydb
import users
import time
import question
import json
from flask import Flask, request, jsonify, render_template


class Queue:
    def __init__(self):
        self.queue_db = tinydb.TinyDB(f'data/queue.json')
        # queue_matadata = {
        #     "_id": -1,
        #     "container": [],
        #     "instructorID": -1,
        #     "location": "Siebel 1404",
        #     "startTime": -1,
        #     "status": False,
        #     "motd": "DummyHead", 
        # }
        # self.queue_db.insert(queue_matadata)

    def add_queue_data(self, qId, instructorID, location, status, motd):
        queue_metadata = {
            '_id': qId,
            'container': [],
            'instructorID': instructorID,
            'location': location,
            'startTime': int(time.time()),
            'status': status,
            'motd': motd
        }
        self.queue_db.insert(queue_metadata)  

    def fetch_queue_by_qid(self, qId):
        if not isinstance(qId, int):
            qId = int(qId)
        results = self.queue_db.search(tinydb.Query()._id == qId)
        if not results:
            return {'error': 'No Queue matching the parameters could be found'}
        return results[0] 

    def create_queue_if_doesnt_exist(self, qId, instructorID, location, status, motd):
        queue_result = self.fetch_queue_by_qid(qId)
        if queue_result:
            return queue_result
        self.add_queue_data(qId, instructorID, location, status, motd)

    def offer(self, qId, questionId):
        queue_result = self.fetch_queue_by_qid(qId)
        queue_container = queue_result.get('container')
        queue_container.append(questionId)
        self.queue_db.update({'container': queue_container}, tinydb.Query()._id == qId)


    def poll(self, qId):
        queue_result = self.fetch_queue_by_qid(qId)
        queue_container = queue_result.get("container")
        poped_value = queue_container.popleft()
        self.queue_db.update({'container': queue_container}, tinydb.Query()._id == qId)
        return poped_value

    def peek(self, qId):
        queue_result = self.fetch_queue_by_qid(qId)
        queue_container = queue_result.get('container')
        if (len(queue_container) == 0):
            return json.dumps("Nobody is in the Queue right now!")
        else:
            return json.dumps(queue_container[0])

    def size(self, qId):
        queue_result = self.fetch_queue_by_qid(qId)
        queue_container = list(queue_result.get("container"))
        return len(queue_container)
    

def debug(keep_changes=False):

    testQ = Queue()
    testQ.add_queue_data(qId=100, instructorID=88, location="Siebel 0220", status=True, motd="Do not copy")
    testQ.add_queue_data(qId=101, instructorID=88, location="Siebel 0224", status=True, motd="Do not copy")
    testQ.offer(100, 1)
    testQ.offer(100, 2)
    testQ.offer(100, 3)

    print(testQ.peek(100))
    if not keep_changes:
        testQ.queue_db.purge()
        print(" > DEBUG: Purged users database")

if __name__ == "__main__":
    debug(False)