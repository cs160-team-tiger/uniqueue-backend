import tinydb
import time
import utils

class OHQueue:
    def __init__(self):
        self.queue_db = tinydb.TinyDB(f'data/queue.json')
        # self.queue_db.DEFAULT_TABLE_KWARGS = {'cache_size': 0}

    def add_queue_data(self, queue_name, instructor_id, location_name, is_open, motd, location_latitude, location_longitude, queue_id=None):
        if not queue_id:
            queue_id = utils.get_next_available_id('queue.json')
        queue_metadata = {
            'queue_name': queue_name,
            '_id': queue_id,
            'question_ids': [],
            'instructor_id': instructor_id,
            'location_name': location_name,
            'start_time': int(time.time()),
            'is_open': is_open,
            'motd': motd,
            'location_latitude': location_latitude,
            'location_longitude': location_longitude
        }
        self.queue_db.insert(queue_metadata) 
        print(f" > DEBUG: Created queue #{queue_id} ('{queue_name}') at {location_name} (Instructor UUID: {instructor_id})")
        return queue_metadata 

    def fetch_queue_by_qid(self, queue_id):
        if not isinstance(queue_id, int):
            queue_id = int(queue_id)
        result = self.queue_db.get(tinydb.Query()._id == queue_id)
        if not result:
            return {'error': 'No queue matching the parameters could be found'}
        return result

    def create_queue_if_doesnt_exist(self, queue_id, queue_name, instructor_id, location_name, is_open, motd, location_latitude, location_longitude):
        queue_result = self.fetch_queue_by_qid(queue_id)
        if queue_result:
            return queue_result
        self.add_queue_data(queue_name=queue_name, instructor_id=instructor_id, location_name=location_name, is_open=is_open,
                            motd=motd, location_latitude=location_latitude, location_longitude=location_longitude, queue_id=queue_id)
    # Question ID management 

    def add_question_id_to_queue(self, queue_id, question_id):
        if not isinstance(queue_id, int):
            queue_id = int(queue_id)
        queue_data = self.fetch_queue_by_qid(queue_id)
        if "error" in queue_data:
            return {"error": f"No queue matching the queue ID {queue_id} could be found while appending question ID {question_id}"}
        if "question_ids" not in queue_data:
            return {"error": f"Malformed queue dict: no entry 'question_ids' in queue {queue_id}"}
        print(f" > DEBUG: Adding question {question_id} from queue {queue_id}")
        queue_data['question_ids'].append(question_id)
        self.queue_db.update({'question_ids': queue_data['question_ids']}, tinydb.Query()._id == queue_id)
        return self.fetch_queue_by_qid(queue_id)

    def remove_question_id_from_queue(self, queue_id, question_id):
        if not isinstance(queue_id, int):
            queue_id = int(queue_id)
        queue_data = self.fetch_queue_by_qid(queue_id)
        if "error" in queue_data:
            return {"error": f"No queue matching the queue ID {queue_id} could be found while removing question ID {question_id}"}
        if "question_ids" not in queue_data:
            return {"error": f"Malformed queue dict: no entry 'question_ids' in queue {queue_id}"}
        if question_id not in queue_data['question_ids']:
            return {"error": f"Could not remove question {question_id} from queue {queue_id}: no entry was found"}
        print(f" > DEBUG: Removing question {question_id} from queue {queue_id}")
        queue_data['question_ids'].remove(question_id)
        self.queue_db.update({'question_ids': queue_data['question_ids']}, tinydb.Query()._id == queue_id)
        return self.fetch_queue_by_qid(queue_id)

    def set_motd(self, queue_id, motd):
        if not isinstance(queue_id, int):
            queue_id = int(queue_id)
        queue_data = self.fetch_queue_by_qid(queue_id)
        if "error" in queue_data:
            return {"error": f"No queue matching the queue ID {queue_id} could be found to set a MOTD"}
        print(f" > DEBUG: Setting queue {queue_id}'s MOTD to '{motd}'")
        self.queue_db.update({'motd': motd}, tinydb.Query()._id == queue_id)
        return self.fetch_queue_by_qid(queue_id)

    def open_queue(self, queue_id):
        if not isinstance(queue_id, int):
            queue_id = int(queue_id)
        queue_data = self.fetch_queue_by_qid(queue_id)
        if "error" in queue_data:
            return {"error": f"No queue matching the queue ID {queue_id} could be found to open"}
        if queue_data['is_open']:
            return {"error": f"Queue {queue_id} is already open!"}
        print(f" > DEBUG: Opening queue {queue_id}")
        self.queue_db.update({'is_open': True}, tinydb.Query()._id == queue_id)
        return self.fetch_queue_by_qid(queue_id)

    def close_queue(self, queue_id):
        if not isinstance(queue_id, int):
            queue_id = int(queue_id)
        queue_data = self.fetch_queue_by_qid(queue_id)
        if "error" in queue_data:
            return {"error": f"No queue matching the queue ID {queue_id} could be found to close"}
        if not queue_data['is_open']:
            return {"error": f"Queue {queue_id} is already closed!"}
        print(f" > DEBUG: Closing queue {queue_id}")
        self.queue_db.update({'is_open': False}, tinydb.Query()._id == queue_id)
        return self.fetch_queue_by_qid(queue_id)

    # Queue Utilities

    # Depricated method!
    # This is currently an almost-duplicate of add_question_id_to_queue.

    # def offer(self, queue_id, question_id):
    #     queue_result = self.fetch_queue_by_qid(queue_id)
    #     queue_container = queue_result.get('question_ids')
    #     queue_container.append(question_id)
    #     self.queue_db.update({'question_ids': queue_container}, tinydb.Query()._id == queue_id)


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

    def fetch_all_queues(self):
        return self.queue_db.all()
    

def debug(keep_changes=False):

    testQ = OHQueue()
    testQ.add_queue_data(queue_id=100, instructor_id=88, location="Siebel 0220", is_open=True, motd="Do not copy", location_latitude=31.231, location_longitude=-131.221)
    testQ.add_queue_data(queue_id=101, instructor_id=89, location="Jacobs 320", is_open=True, motd="If you feel the need to cry, please step outside.", location_latitude=21.431, location_longitude=-111.441)
    testQ.offer(100, 1)
    testQ.offer(100, 2)
    testQ.offer(100, 3)

    print(testQ.peek(100))
    if not keep_changes:
        testQ.queue_db.purge()
        print(" > DEBUG: Purged queue database")

# if __name__ == "__main__":
#     debug(False)