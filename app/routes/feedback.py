# This file contains all the routes for the Feedback functionality

from app import app
from flask import render_template, redirect, url_for, request, session, flash
# This imports the data classes your created in the data file in the classes folder
from app.classes.data import Post, Comment, Feedback, User
# This imports all the needed forms classes from the forms file in the classes folder
from app.classes.forms import PostForm, CommentForm, FeedbackForm
import datetime as dt
from bson.objectid import ObjectId
# this imports the admins list from the users.py file
from .users import admins

# This route lists all of the feedback records. The first line triggers this code when the user asks for your
# webpage ending in '/feedbackall'. 
@app.route('/feedbackall')
# Define the function that is to be run.
def feedbackall():
    # call the class your created in the data file in the classes folder and retrieve all of the
    # feedback records in an object. 
    fbacks = Feedback.objects()
    # end the function and send all the feedback records (fbacks) that were retrieved to the fedbackall.html template
    return render_template("feedbackall.html", fbacks=fbacks)

# This route retrieves for display one feedback item
@app.route('/feedback/<feedbackid>')
def feedback(feedbackid):
    # the 'get' method in the code below expects to receive only one record.  The attribute 'pk' stands for
    # primary key wich is the objectid for the record you want to retrieve.  The feedbackid is passed in to this function
    # as a parameter from the url and then in to the function and then used to ask for a specific feedback id via the get
    # method
    fback = Feedback.objects.get(pk=feedbackid)
    # Here is the get method used again to retrive the object that is the user that has requested this specific feedbackid.
    # The current user ID is being stored in the session.  You can see how that is done in the user.py file.
    currUser = User.objects.get(gid=session['gid'])
    # Each feedback record can have a conversation attached to it. These convesations are post and comment objects.
    # In python using 'try:' is a way to capture if an error happens and if it does then do something else --> 'except:'
    # This try will cause an error if there is no post record attached to the feedback item.  If it fails, the except
    # part will set fbackposts to 'none'.  If the try does not fail, it will put all of the posts in the fbackposts object.
    try:
        fbackposts = Post.objects(feedback = feedbackid)
    except:
        fbackposts = None
    # the next line ends the function and calls for the feedback.html template and sends several variables
    # that can then be displayed on the template.
    return render_template('feedback.html', fback=fback, currUser=currUser, fbackposts=fbackposts)

# This route creates a new feedback record. The 'url' parameter is collected from the "new feedback" link that is created 
# in the navbar and the user clicks it and the url parameter is passed to the newfeedback function on the second line below.
# take a look at the navbar in templates, includes to see how the url is created. Because it is a form you need the 'GET' and
# POST methods.
@app.route('/newfeedback/<url>', methods=['GET', 'POST'])
# You can add a default value to a parameter that will be used if the parameter is not passed from the url. Below, if the 
# the parameter is not passed it is because they came from the home page so I put it here.
def newfeedback(url):

    # This instantiates the form object and creates an object that contains all the methods and attributes of the FeedbackForm class
    form = FeedbackForm()
    # this is a hacky piece of code that makes it possible to store the 'path' of the page that the feedback is about.
    # the 'zzz' part you can find in the navbar where the "new Feedback" link is.
    form.url.data=url.replace('zzz','/')

    # form.validate_on_submit() is a method of the form object that simply returns True of False.
    # Returning true means that the user filled out the form and that all the validations and definitions
    # placed on the form data by the form object checked out and the submission is valid. So, if the 
    # user submitted valid data, we now want to save that data to the database. 
    if form.validate_on_submit():

        # This is instantiating an 'empty' feedback object and placing data from the form into that new object
        newFeedback = Feedback(
            # The attribute on the left of the = is the name of the filed as defined in the Feedback data class 
            # the variable on the left is how you refer to what was collected from the form and placed in the 
            # form object.
            priority=form.priority.data,
            subject=form.subject.data, 
            body=form.body.data, 
            solution=form.solution.data,
            # This is not collected from the user but is input here as the exact date and time the record is created
            createdate=dt.datetime.now(),
            url=form.url.data,
            # This is also not enterred by the user but instead is taken from the session values. An ObjectId is a special
            # type of data. the ObjectId() method below turns a string in to an ObjectId. Each time a user logs in
            # a new session is started and certain values are stored in it including the users Id # for the site which 
            # can be referenced as session['currUserId'].  If you look at the profile page on the site you can see
            # all the session values available.
            author=ObjectId(session['currUserId']),
            status=form.status.data
        )
        # Once the object is filled with the data from the form you then save it to the database.
        newFeedback.save()
        # flash is a Flask command that sends messages back to the website. The message shows up on whatever page the user next sees.
        # The code that displays that message is on the base.html template.
        flash('Thank you for the feedback!')
        # after it is saved it is always a good idea to reload it from the database to make sure you 
        # have all the correct values in the correct way.
        newFeedback.reload()
        # Once the newFeedback is saved and reloaded the code below returns the new feedback id string to the feedback function above.
        # The redirect() method is part of Flask and it redirects the code to another function.  The url_for() function
        # is also part of Flask and it creates the url that is needed for the @app.route('/feedback/<feedbackid>') above.
        return redirect(url_for('feedback', feedbackid=newFeedback.id))

    # The following code is run if form.validate_on_submit() from above is 'False'. That would be true is two situations. It could be 
    # that the user tried to submit the form but it didn't work.  More likely it is because the user has not yet submit the form and is 
    # calling this route in order to get and fill out the empty form to submit it.  The flash command send a msg to the user.
    flash('Fill out the form to provide some feedback on this site.')
    # The code below returns the template feedbackform.html and sends the 'form' object to be displayed.
    return render_template('feedbackform.html', form=form)

# The next route is for editing existing feedback records. It is very similar to creating a new feedback record except it has to first 
# populate the form with existing data. Because it is a from you need both the 'GET' and 'POST' methods. Because the code
# edits a specific feedback record we need the id of the record to retreive it from the database.  Checkout the feedbacks.html template
# to see how the url is created that passes this information to this route.
@app.route('/editfeedback/<feedbackid>', methods=['GET', 'POST'])
def editfeedback(feedbackid):

    # get the current users object to check if this user has the authority to edit this record
    currUser = User.objects.get(gid=session['gid'])
    # get the feedbackForm from the FeedbackForms class in the forms file in the classes folder.
    form = FeedbackForm()
    # get the intended feedback record that is associated with the feedbackid that is passed in to this route. To do this you 
    # use the mongoengine get() method to ensure you are getting only one record. pk means primary key and is the generic
    # term for the id of any mongoengine record. 
    editFback = Feedback.objects.get(pk=feedbackid)

    # Check that the user has the appropriate privleges to edit this record.  Either they are the original author and
    # the feedback is still in the new status or the user is an admin as designated by a list in users.py file in routes.
    if not (currUser.id == editFback.author.id and editFback.status == "4-New") and not currUser.email in admins:
        # If this fails then tell the user they can't edit the file and send them back to the feedback's record.
        flash(f'You cannot edit this job..')
        return redirect(url_for('feedback',feedbackid=editFback.id))

    # If the form has been submitted and it is valid then the method validate_on_submit() will be True
    if form.validate_on_submit():
        # The mongoengine update() method changes existing values in the database
        editFback.update(
            # the attributes of the left are the data field names
            # the value on the right are the values from the valid form submission
            priority=form.priority.data,
            subject=form.subject.data, 
            body=form.body.data, 
            solution=form.solution.data,
            # This value is not assigned by user but is automatically assigned by the datetime python module
            modifydate=dt.datetime.now(),
            status=form.status.data,
            url=form.url.data
        )
        # once the update() method is run, then run reload() to get all the updated data.
        editFback.reload()
        # use flash to send a msg back to the user
        flash('You have updated the infomation on this Job.')
        # redirect the user to the new feedback record 
        return redirect(url_for('feedback',feedbackid=editFback.id))

    # if form.validate_on_submit() is false then present the use with the form that is pre-populated with 
    # values from the database.  Start by sending a message to the user with the flash command.
    flash('Change the values in the fields to edit this feedback')
    # When you create an empty form object then all the data attributes of each field are empty. The followng code
    # places data from the feedback object that was retrieved in to the data attributes of the form object so that
    # when the form is rendered on the template the fields are prepopulated with the data from the feedback record to be edited
    form.priority.data=editFback.priority
    form.subject.data=editFback.subject
    form.body.data=editFback.body
    form.solution.data=editFback.solution
    form.url.data=editFback.url
    form.status.data=editFback.status
    # send the user to the pre-populated feedback form
    return render_template('feedbackform.html', form=form)

# this final route will delete an existing feedback record
@app.route('/deletefeedback/<feedbackid>')
def deletefeedback(feedbackid):

    # retrieve the feedback object to be deleted
    deleteFback = Feedback.objects.get(pk=feedbackid)
    # load the current user's object to check if they are allowed to delete the feedback record
    currUser = User.objects.get(gid=session['gid'])

    # check if the current user is the author of the feedback and it is still n new status or the current user is an admin
    if not (currUser.id == deleteFback.author.id and deleteFback.status == "4-New") and not currUser.email in admins:
        # if they do not have the right provleges send them back to the feedback
        flash(f'You cannot delete this job.')
        return redirect(url_for('feedback', feedbackid=deleteFback.id))

    # If they do have the privleges then do the delete thang and send the user to a list of all remaining feedback records
    deleteFback.delete()
    return redirect(url_for('feedbackall'))
