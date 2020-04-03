# This file defines all of the forms that are used in the app. A form is a way for the user to add
# new data or to edit exoisting data. Forms are classes
# so each form is created as an object that can then be displayed on a template by referring to the 
# attributes of the objects.

# wtforms is the library that manages this and has good docs and help on stackexchange
# the imports here are for wtforms and various other wtforms components
from flask_wtf import FlaskForm
from wtforms.fields.html5 import URLField, DateField
from wtforms_components import TimeField
from wtforms.validators import url
from wtforms import StringField, SubmitField, validators, TextAreaField, HiddenField, IntegerField, SelectField

# This is the form for creating and updating users. The fields that are listed here in the UserForm
# are the one's that the user is allowed to create and edit. You can see how this form is shown to the user in the 
# edituser.html template. You can see how the editing and creating users is done in the users.py route specifically
# in the /login and the /edituser routes in the user.py file. 
class UserForm(FlaskForm):
    # 'fname' is how the form field is refered to in the code.  StringField is the field type
    # and "First Name" is what is printed on the webpage via the template to lable the field 
    fname = StringField("First Name")
    lname = StringField("Last Name")
    # A SelectField is how you create a dropdown list of values.  Each value in the dropdown
    # is a tuple with two values. The first is what is stored in the database record the second
    # is what is shown in the dorwpdown list.  Most of the time they are the same.  
    pronouns = SelectField(choices=[('He/Him', 'He/Him'),('She/Her','She/Her'),('They/Them','They/Them'),('Any/All','Any/All')])
    # The image field is not an upload of an image file but instead is a link to an image that is publically
    # available on the web. The is a vlaidator that checks that is is a propoerly formatted url. 
    image = URLField('Image URL', validators=[url()])
    birthdate = DateField()
    # all forms must have a submit
    submit = SubmitField("Submit")

# This is the form for creating and editing a Post.
class PostForm(FlaskForm):
    subject = StringField("Title")
    # a textAreaField is a large text field
    body = TextAreaField("Body")
    submit = SubmitField("Submit")

# This is the form for creating a comment on a Post.
class CommentForm(FlaskForm):
    comment = TextAreaField("Comment")
    submit = SubmitField("Submit")

class EventForm(FlaskForm):
    title = StringField("Title")
    desc = StringField("Description")
    # There are a lot of ways to record an manage date and time.  The way I have here is the easiest to understand
    date = DateField("Date", format='%Y-%m-%d')
    time = TimeField("Time")
    submit = SubmitField("Submit")

class FeedbackForm(FlaskForm):
    url = StringField()
    subject = StringField('Subject')
    body = TextAreaField('Description')
    solution = TextAreaField('Solution')
    status = SelectField("Status", choices=[('4-New','4-New'),('1-In Progress','1-In Progress'),('2-Complete','2-Complete'),('3-Maybe Someday','3-Maybe Someday')], default='4-New')
    priority = SelectField("Priority", choices=[('1-High','1-High'),('2-Medium','2-Medium'),('3-Low','3-Low')], default='3-Low')
    submit = SubmitField('Submit')