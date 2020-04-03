'''
This file is where all the data collections are described.  Each data collection is a Class and the values 
listed here are the attributes of the class.  There are also many methods that are described by a parent class
that is called mongoengine. When you ask a question about data (ie give me all the students in a class).  That data
is returned as an object.  

Mongoengine is the library that manages all this and their docs are very good and Stackoverflow does a great 
job of making it easy to to do the basic stuff
'''
# When you import mongoengine you also have to import each of the different field types that you will use.  I will describe these below
# where I use them.  Some of them like StringField and IntField are obvious. When you use these fields below they are used as methods
# which simply means that you use '()' after the field name like 'StringField()'. You can find all of the mongoengine fields here
# http://docs.mongoengine.org/apireference.html#fields
from mongoengine import Document, StringField, IntField, BooleanField, ReferenceField, EmbeddedDocumentField, DateTimeField, DateField, EmailField, URLField, ListField, CASCADE
import datetime as d

# This class is what creates the databse document where all user information is stored.
class User(Document):
    # Values copied from the Google Account or input by code. I recommend NOT editing the values in these fields
    # because you can't edit them in their origins. Instead, I created copies of the fields that I want to give
    # the user the ability to edit. 
    # First four fields are the user's first name, last name, email and Google ID # that are copied from Google in the User.py routes file.
    gfname = StringField()
    glname = StringField()
    # Mongoengine has several field types like email field that enable you to varify that what the user put in is actually 
    # that type of data like EmailField() below.  
    email = EmailField()
    # unique is a parameter that is possible on all fields. it is false by default. If you want to make sure that each
    # vlaue in a field is unique that you need to set this to True. In this case gid is the users googleID and no two
    # users can have the same gid.
    gid = StringField(unique=True)
    # The role value is enterred by the code in the user.py routes based on if the user's email as an 's_' at the beginning.
    # The roles are "teacher" or "Student"
    role = StringField()
    # In the users.py file there is a python list of email addresses of people designated to be "admins" of this app.
    # so that user has some special privleges.
    admin = BooleanField()
    # The following values are all set in the users.py file.  these fields can all be edited by the user in the edit profile function.
    pronouns = StringField()
    fname = StringField()
    lname = StringField()
    # URLField() holds a URL or a link to a webpage
    image = URLField()
    # DateField() holds just a date.  There is also a DateTimeField()
    birthdate = DateField()
    # This is how you set the default sorting.  You can also sort records after you retreive them in the route.
    meta = {
        'ordering': ['+lname', '+fname']
    }

# This class is what creates the Feedback document in the database.
# A feedback is defined as a comment by a user on some feature of the website. 
# Feedback is created and edited using the FeedbackForm in the forms.py file. That form is presented
# to the web user via the feedbackform.html template and the feedback.py routes file specifically the
# /newfeedback and /updatefeedback routes manage the process.
class Feedback(Document):
    # Each feedback document has exactly one author.  The author field on the feedback document is a reference to 
    # a user that is in the User Document.  This is what a ReferenceField() does.  The reverse_delete_rule means that
    # if you delete a user, also delete all the feedback records. 
    author = ReferenceField(User,reverse_delete_rule=CASCADE)
    # These fields are updated not by the user but by the code in the feedback.py routes file specifically in the
    # /newfeedback and /updatefeedback routes
    createdate = DateTimeField(default=d.datetime.utcnow)
    modifydate = DateTimeField()
    # This is a stringField() and not a url field because it is not a full URL. This field is designed to be an identifyier
    # of the page that the feedback is about.
    url = StringField()
    # the subject of the feedback
    subject = StringField()
    # Further description of the feedback
    body = StringField()
    # what status in the feedback in ie new, in progress, complete...
    status = StringField()
    # what is the developers priority for implementing the feedback
    priority = StringField()
    # notes about how to solve the feedback
    solution = StringField()

    meta = {
        'ordering': ['+status','+priority', '+createdate']
    }

# a post can be any communication from the website user.  Comments, 
# the next class in this file, is a comment
# on a post.
class Post(Document):
    # A post is created by a user (maybe 'author' would be a better 
    # name for this field). This field is a 
    # ReferenceField() back to the user document.
    user = ReferenceField(User,reverse_delete_rule=CASCADE)
    # Because posts in this site are always related to fedback records, 
    # there is a RefereceFireld that connects 
    # posts to Feedbacks.  
    feedback = ReferenceField(Feedback)
    subject = StringField()
    body = StringField()
    createdate = DateTimeField(default=d.datetime.utcnow)
    modifydate = DateTimeField()

    meta = {
        'ordering': ['+createdate']
    }

# Comments are always comments on posts so they are always related to posts.
class Comment(Document):
    comment = StringField()
    createdate = DateTimeField(default=d.datetime.utcnow)
    modifydate = DateTimeField
    # REference to the post
    post = ReferenceField(Post,reverse_delete_rule=CASCADE)
    # Reference to the user who is the author of this comment
    user = ReferenceField(User,reverse_delete_rule=CASCADE)
    
    meta = {
        'ordering': ['+createdate']
    }

# Events are items that are displayed on the calendar.  The fields are very simple and
# and can easily be changed to add other information that you want. 
class Event(Document):
    # All events have 'owners' which are a referencefield connected to the User document
    owner = ReferenceField(User)
    title = StringField()
    desc = StringField()
    date = DateTimeField()

    meta = {
        'ordering': ['+date']
    }