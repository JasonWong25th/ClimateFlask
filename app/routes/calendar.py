# This file contains all the routes that control the calendar functionality
# Be careful editing this file. For the most part I would leave alone all code 
# that draws the calendar, Week, Day.  The Event code is is where you can make
# your edits.

# For a thorough description of how to do stuff, go to the feedback.py file

from app.routes import app
from flask import render_template, session, redirect, request, flash
import calendar
import datetime as d
# This imports the data objects that you created in the data file in the classes folder
from app.classes.data import Event, User
# This imports the forms that you created in the forms file in the classes folder
from app.classes.forms import EventForm
from bson.objectid import ObjectId

cal = calendar.Calendar(6)

# mormal and reverse month dictionaries
months = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
reverseMonths = {v: k for k, v in months.items()}


# Get today's month and year if there are no arguments
# Get day for calendar display
currentday = str(d.datetime.now().day)
currentmonth = str(d.datetime.now().month)
currentyear = str(d.datetime.now().year)


# functions to load a list for a month and is called from the getMonth function
def flatten(array):
    new = []
    for i in array:
      for j in i:
        new.append(j)
    return new

# Gets month data from the calendar library which is imported above
def getMonth(month, year):
    weeks = cal.monthdayscalendar(int(year), months[month])
    return flatten(weeks)


# multiple @app.route decorators can be used to catch multiple combinations of url's input by the user
@app.route('/calendar', methods=['GET', 'POST'],  defaults={'month': reverseMonths[int(currentmonth)], 'year': currentyear})
@app.route('/calendar/<month>/<year>', methods=['GET', 'POST'])
def calen(month, year):
    if 'credentials' not in session:
        flash('You must be logged in to access that page')
        return redirect('authorize')
    # Manages looping the months and going to the next Year
    nextMonthYear = year
    prevMonthYear = year
    nextMonth = (months[month]+1)
    prevMonth = (months[month]-1)
    if month == "December":
        nextMonthYear = str(int(year)+1)
        nextMonth = 1
    elif month == "January":
        prevMonthYear = str(int(year)-1)
        prevMonth = 12

    nextMonthName = reverseMonths[nextMonth]
    prevMonthName = reverseMonths[prevMonth]
    nextYear = str(int(year)+1)
    prevYear = str(int(year)-1)


    #get events and format the dates for use on the calendar
    events = Event.objects()
    for event in events:
        event.date = event.date.strftime('%Y-%m-%d').split("-")
        event.date[1] = reverseMonths[int(event.date[1])]
        event.date[2] = str(int(event.date[2]))


    return render_template('calendar.html', monthName = month, nextMonthName = nextMonthName, prevMonthName = prevMonthName,
    month=getMonth(month, year), year=year, nextYear = nextYear, prevYear = prevYear, nextMonthYear = nextMonthYear, prevMonthYear = prevMonthYear,
    weekdays=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
    events=events,
    currentday=currentday, currentmonth=currentmonth, monthNameReverse = months[month], currentyear=currentyear)

# this is the code that is run when the user requests a specific day
@app.route('/day/<day>/<month>/<year>', methods=['GET', 'POST'])
def day(day, month, year):

    if 'credentials' not in session:
        flash('You must be logged in to access that page')
        return redirect('authorize')

    #get events and format the dates for use on the calendar
    events = Event.objects()
    for event in events:
        event.date = event.date.strftime('%Y-%m-%d-%I:%M %p').split("-")
        event.date[1] = reverseMonths[int(event.date[1])]
        event.date[2] = str(int(event.date[2]))

    return render_template('day.html', day=day, month=month, year=year, events=events)

# TODO need an editEvent route

# this function is run when the user requests to delete an event.
@app.route('/deleteevent/<id>', methods=['GET', 'POST'])
def deleteevent(id):

    if 'credentials' not in session:
        flash('You must be logged in to access that page')
        return redirect('authorize')

    for event in Event.objects:
        if str(event.id) == id:
            event.delete()
            return redirect('/calendar')
    return render_template("index.html")

# This code is run when the user wants to create a new event
@app.route('/newevent', methods=['GET', 'POST'])
@app.route('/newevent/<objtype>/<objid>', methods=['GET', 'POST'])
def newevent(objtype="none",objid="none"):
    if 'credentials' not in session:
        flash('You must be logged in to access that page')
        return redirect('authorize')
    form = EventForm()
    if form.validate_on_submit():
      eventtime = str(form.time.data)
      eventtime = eventtime.split(":")
      eventdate = form.date.data
      eventdate = eventdate.strftime('%Y-%m-%d').split("-")
      eventdatetime = d.datetime.combine(d.date(int(eventdate[0]),int(eventdate[1]),int(eventdate[2])), d.time(int(eventtime[0]),int(eventtime[1]),int(eventtime[2])))

      newEvent = Event()
      newEvent.owner = ObjectId(session['currUserId'])
      newEvent.title = form.title.data
      newEvent.desc = form.desc.data
      newEvent.date = eventdatetime
      newEvent.save()

      newEvent.reload()

      if objtype == "job" and objid:
        newEvent.update(job=ObjectId(objid))

      return redirect('/calendar')

    return render_template('newevent.html', form=form)
