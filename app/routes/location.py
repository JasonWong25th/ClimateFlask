from app import app
from flask import Flask,render_template,redirect,session, url_for,flash
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,IntegerField,validators
from flask_wtf.file import FileField, FileRequired , FileAllowed
import os
from app.classes.locationData import LocationData
from app.classes.data import User
from bson.objectid import ObjectId

import datetime as dt

class LocationForm(FlaskForm):
    name = StringField("What's the location's name")
    desc = StringField("What is the description")
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