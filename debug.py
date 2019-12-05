from users import Users
from questions import Questions
from ohqueue import OHQueue
from controller import Controller

users = Users()
questions = Questions()
ohqueue = OHQueue()
controller = Controller()

def add_debug_users():
    # 87-89: Instructors
    # 90-98: Students
    users.create_user_if_doesnt_exist(
        uuid=87,
        name="Oski Bear",
        email="test@berkeley.edu")
    users.create_user_if_doesnt_exist(
        uuid=88,
        name="Nellie Robertson",
        email="testA@berkeley.edu")
    users.create_user_if_doesnt_exist(
        uuid=89,
        name="Hubert Perkins",
        email="testB@berkeley.edu")
    users.create_user_if_doesnt_exist(
        uuid=90,
        name="Jackie McCoy",
        email="testC@berkeley.edu")
    users.create_user_if_doesnt_exist(
        uuid=91,
        name="Karl O'Brien",
        email="testD@berkeley.edu")
    users.create_user_if_doesnt_exist(
        uuid=92,
        name="Jose Walters",
        email="testE@berkeley.edu")
    users.create_user_if_doesnt_exist(
        uuid=93,
        name="Nazia Winter",
        email="testF@berkeley.edu")
    users.create_user_if_doesnt_exist(
        uuid=94,
        name="Kailan Alvarez",
        email="testG@berkeley.edu")
    users.create_user_if_doesnt_exist(
        uuid=95,
        name="Aaliyah Stark",
        email="testH@berkeley.edu")
    users.create_user_if_doesnt_exist(
        uuid=96,
        name="James Turner",
        email="testG@berkeley.edu")
    users.create_user_if_doesnt_exist(
        uuid=97,
        name="Poppy Chapman",
        email="testH@berkeley.edu")
    users.create_user_if_doesnt_exist(
        uuid=98,
        name="Adam Savidan",
        email="testI@berkeley.edu")
    users.create_user_if_doesnt_exist(
        uuid=655677096,
        name="Peng Gu",
        email="peng@berkeley.edu")
    users.create_user_if_doesnt_exist(
        uuid=3035324241,
        name="Sundi Xiao",
        email="sundi@berkeley.edu")
    users.create_user_if_doesnt_exist(
        uuid=3031811472,
        name="David Xiong",
        email="david@berkeley.edu")
    users.create_user_if_doesnt_exist(
        uuid=3035323669,
        name="Jiewen Lai",
        email="jiewen@berkeley.edu")
    users.create_user_if_doesnt_exist(
        uuid=3035324150,
        name="Zoey Cao",
        email="jiewen@berkeley.edu")

def add_debug_queues():
    ohqueue.add_queue_data( # ID: 100
        queue_name="Oski - CS61A", 
        instructor_id=87, 
        location_name="Jacobs 210", 
        is_open=True, 
        motd="Project 4 due next Tuesday. Ask Miriam if you have questions about homework.", 
        location_latitude=0, location_longitude=0)
    ohqueue.add_queue_data( # ID: 101
        queue_name="Nellie's CS61B OH", 
        instructor_id=88, 
        location_name="Soda 421", 
        is_open=True, 
        motd="Welcome to office hours! We're focusing on midterm questions for today, but feel free to queue for anything.", 
        location_latitude=0, location_longitude=0)
    ohqueue.add_queue_data( # ID: 102
        queue_name="CS160 Office Hours (Hubert)", 
        instructor_id=89, 
        location_name="Soda 210", 
        is_open=True, 
        motd="Everyone feeling ready for their final presentations? I'll be helping debug your apps today.", 
        location_latitude=0, location_longitude=0)
    ohqueue.add_queue_data( # ID: 103
        queue_name="David's OH - CS198-01", 
        instructor_id=30318111472, 
        location_name="Cory 351", 
        is_open=True, 
        motd="If you must cry, please do so outside.", 
        location_latitude=0, location_longitude=0)


def add_debug_questions():
    # Oski's CS61A OHs
    controller.add_question_to_queue( # 100
        queue_id=100, 
        student_uuid=90, 
        question_text="HW 10 Q3: How do I get the size of a dog and its sibling in one select statement? ")
    controller.add_question_to_queue(
        queue_id=100, 
        student_uuid=98, 
        question_text="Any hints for how to approach make_s? The hint says elements of scale_stream(s, 2) are elements of s, but s is what we're trying to make, so how do I use this hint?")
    controller.assign_image_to_question(101, "static/question_assets/101_q5screenshot.jpg")
    controller.add_question_to_queue(
        queue_id=100, 
        student_uuid=94, 
        question_text="Does the group by clause end up randomly selecting one element from the group if no aggregate functions are used? It seems that the numbers of possibilities are reduced when using group by clause (without any other adjustments)")
    controller.add_question_to_queue(
        queue_id=100, 
        student_uuid=91, 
        question_text="How do I use map_stream function? Should I use it as an argument?")
    controller.add_question_to_queue(
        queue_id=100, 
        student_uuid=96, 
        question_text="How can we use the ith element of the stream if we are constructing the stream at the same time? Wouldn't we be looking for something that doesn't yet exist?")

    # Nellie's CS61B OHs
    controller.add_question_to_queue(
        queue_id=101, 
        student_uuid=91, 
        question_text="[Proj 3] For checking if a node's dependencies are built, do we just check if each dependency exists in the dependency graph and recursively check on their dependencies? ")
    controller.add_question_to_queue(
        queue_id=101, 
        student_uuid=97, 
        question_text="Proj 3: Is it reasonable to have the EdgeSize() method go through the data structure where edges are stored (for me it's an adjacency matrix 2d java array) and count them?  I know this is very slow runtime wise but I don't actually use this method anywhere else in my code.")
    controller.add_question_to_queue( # 107 (currently)
        queue_id=101, 
        student_uuid=98, 
        question_text="Fall 2009 1a - Why doesn't Queue Q3 include 1?")
    controller.assign_image_to_question(107, "107_Screen_Shot_20161212_at_1.06.02_PM.png")
    controller.add_question_to_queue(
        queue_id=101, 
        student_uuid=94, 
        question_text="In the solutions for discussion 11, isn't this a right leaning red-black tree? I thought we're only supposed to have left-leaning ones?")
    controller.assign_image_to_question(108, "108_Screen_Shot_20161212_at_12.16.41_PM.png")
    controller.add_question_to_queue(
        queue_id=101, 
        student_uuid=96, 
        question_text="Why is it that negative edges don't have an effect on Kruskals/Prims? ")
    controller.add_question_to_queue(
        queue_id=101, 
        student_uuid=92, 
        question_text="Why is this a counting sort?")
    controller.assign_image_to_question(110, "110_IMG_0005.jpeg")
    controller.add_question_to_queue(
        queue_id=101, 
        student_uuid=95, 
        question_text="Do we have to deal with isolated vertices in the graph library implementation?")

    # Hubert's CS160 OH
    controller.add_question_to_queue(
        queue_id=102, 
        student_uuid=95, 
        question_text="It looks like Places API will charge you if you want to get the phone number and opening hours of a place. Is there a work around? Or can we hardcode phone number and hours.")
    controller.add_question_to_queue(
        queue_id=102, 
        student_uuid=93, 
        question_text="Is there any benefit in using a MapFragment over a MapView or vice versa? I am trying to use a MapFragment but am struggling to properly access the API. Are there any tips as to how to properly set up a MapFragment?")
    controller.add_question_to_queue(
        queue_id=102, 
        student_uuid=90, 
        question_text="I followed the location services tutorial to get the current device location. However, the latitude and longitude I got back from getLastLocation() are correct since I printed them out, but the map displayed is at Googleplex in Mountain View.")

    # David's CS160 OH
    controller.add_question_to_queue(
        queue_id=103, 
        student_uuid=94, 
        question_text="I'm having trouble on part 3 retrieving the information to create each new 'thisPost'. The way I understand it, the variable 'posts' is a dictionary of [postID : Post]. However, when I try to retrieve the Post, I get an 'AnyObject' which doesn't have the postImagePath, thread etc. information that I need to create a new Post. How do I get this information?")
    controller.add_question_to_queue(
        queue_id=103, 
        student_uuid=97, 
        question_text="I am trying to add users to my database and keep getting an error. I see that after creating the account, a user is added to 'Authentication' but it seems that nothing is actually added to my database. My database is set up so that anyone can make modifications. I'm not sure what the problem can be.")

def add_debug_activity():
    pass

def reset_data():
    users.users_db.purge()
    ohqueue.queue_db.purge()
    questions.question_db.purge()
    add_debug_users()
    add_debug_queues()
    add_debug_questions()
    add_debug_activity()