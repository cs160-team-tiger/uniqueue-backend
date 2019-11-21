import tinydb
import time

class OHQueue:
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

    def add_queue_data(self, queue_id, instructor_id, location, status, motd):
        queue_metadata = {
            '_id': queue_id,
            'question_ids': [],
            'instructor_id': instructor_id,
            'location': location,
            'startTime': int(time.time()),
            'status': status,
            'motd': motd
        }
        self.queue_db.insert(queue_metadata)  

    def fetch_queue_by_qid(self, queue_id):
        if not isinstance(queue_id, int):
            queue_id = int(queue_id)
        results = self.queue_db.search(tinydb.Query()._id == queue_id)
        if not results:
            return {'error': 'No queue matching the parameters could be found'}
        return results[0] 

    def create_queue_if_doesnt_exist(self, queue_id, instructor_id, location, status, motd):
        queue_result = self.fetch_queue_by_qid(queue_id)
        if queue_result:
            return queue_result
        self.add_queue_data(queue_id, instructor_id, location, status, motd)

    def offer(self, queue_id, question_id):
        queue_result = self.fetch_queue_by_qid(queue_id)
        queue_container = queue_result.get('question_ids')
        queue_container.append(question_id)
        self.queue_db.update({'question_ids': queue_container}, tinydb.Query()._id == queue_id)


    def poll(self, queue_id):
        queue_result = self.fetch_queue_by_qid(queue_id)
        queue_container = queue_result.get('question_ids')
        popped_value = queue_container.popleft()
        self.queue_db.update({'question_ids': queue_container}, tinydb.Query()._id == queue_id)
        return popped_value

    def peek(self, question_id):
        queue_result = self.fetch_queue_by_qid(question_id)
        queue_container = queue_result.get('question_ids')
        if (len(queue_container) == 0):
            return {'error': 'Nobody is in the queue right now'}
        else:
            return queue_container[0]

    def size(self, question_id):
        queue_result = self.fetch_queue_by_qid(question_id)
        queue_container = list(queue_result.get("question_ids"))
        return len(queue_container)
    

def debug(keep_changes=False):

    testQ = OHQueue()
    testQ.add_queue_data(queue_id=100, instructor_id=88, location="Siebel 0220", status=True, motd="Do not copy")
    testQ.add_queue_data(queue_id=101, instructor_id=89, location="Jacobs 320", status=True, motd="If you feel the need to cry, please step outside.")
    testQ.offer(100, 1)
    testQ.offer(100, 2)
    testQ.offer(100, 3)

    print(testQ.peek(100))
    if not keep_changes:
        testQ.queue_db.purge()
        print(" > DEBUG: Purged queue database")

if __name__ == "__main__":
    debug(False)