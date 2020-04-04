from app import app
from flask import render_template, redirect, url_for, request, session, flash
from app.classes.data import Post, Comment, Feedback
from app.classes.forms import PostForm, CommentForm
from requests_oauth2.services import GoogleClient
from requests_oauth2 import OAuth2BearerToken
import requests
import datetime as dt
from bson import ObjectId

#Routing for the globe

@app.route('/globe/<currUserName>', methods=['GET', 'POST'])
def globe(currUserName):
    flash(f'Welcome {currUserName}.  This is your globe.')
    return(render_template("globe.html"))
