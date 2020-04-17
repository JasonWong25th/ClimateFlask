from app import app
from flask import Flask,render_template,redirect,session, url_for,flash
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,IntegerField,validators
from flask_wtf.file import FileField, FileRequired , FileAllowed
import os
from app.classes.locationData import LocationData
from app.classes.data import User
from .users import admins
from bson.objectid import ObjectId

import datetime as dt

class LocationForm(FlaskForm):
    name = StringField("Location's name")
    desc = StringField("Location's description")
    image = FileField('image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    longitude = IntegerField("Enter the Longitude")
    latitude = IntegerField("Enter the Latitude")
    submit = SubmitField("Submit")

@app.route('/viewlocationinput/<locationid>')
def viewlocationinput(locationid):
    m_locationData = LocationData.objects.get(pk = locationid)
    currUser = User.objects.get(gid=session['gid'])
    return render_template('viewlocationinput.html', locationData=m_locationData, currUser=currUser)

@app.route('/locationForm', methods = ['GET', 'POST'])
def locationForm():
    form = LocationForm()

    if form.is_submitted():
        print("I work")
        m_locationData = LocationData(
            author=ObjectId(session['currUserId']),
            name = form.name.data,
            desc = form.desc.data,
            createdate = dt.datetime.now(),
            image = form.image.data,
            longitude = form.latitude.data,
            latitude = form.latitude.data
        )
        m_locationData.save()
        m_locationData.reload()
        #flash("You clicked submit")
        return redirect(url_for("viewlocationinput",locationid = m_locationData.id))
        #return render_template("newsFeed.html")
    return render_template('locationform.html', form = form)

@app.route('/editLocationData/<locationid>')
def editLocationData(locationid):
    currLocationData = LocationData.objects.get(pk = locationid)
    form = LocationForm()
    if form.validate_on_submit():
        currLocationData.update(
            name = form.name.data,
            desc = form.desc.data,
            image = form.image.data,
            longitude = form.latitude.data,
            latitude = form.latitude.data
        )
        currLocationData.reload()
        return redirect(url_for("viewlocationinput",locationid = currLocationData.id))

    flash('Change the values in the fields to edit this feedback')
    form.name.data = currLocationData.name
    form.desc.data = currLocationData.desc
    form.image.data = currLocationData.image
    form.longitude.data = currLocationData.longitude
    form.latitude.data = currLocationData.latitude
    # send the user to the pre-populated feedback form
    return render_template('feedbackform.html', form=form)

@app.route('/deleteLocationData/<locationid>')
def deleteLocationData(locationid):
    currLocationData = LocationData.objects.get(pk = locationid)
    # load the current user's object to check if they are allowed to delete the feedback record
    currUser = User.objects.get(gid=session['gid'])

    # check if the current user is the author of the feedback and it is still n new status or the current user is an admin
    if not (currUser.id == currLocationData.author.id ) and not currUser.email in admins:
        # if they do not have the right provleges send them back to the feedback
        flash(f'You cannot delete this job.')
        return redirect(url_for('feedback', locationid = currLocationData.id))
    
    currLocationData.delete()
    return redirect(url_for('allLocationData'))

@app.route('/allLocationData')
def allLocationData():
    allLocationDatas = LocationData.objects()
    return render_template('allLocationData.html',allLocationDatas = allLocationDatas)