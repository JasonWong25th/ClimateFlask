from app import app
from flask import render_template, redirect, url_for, request, session, flash
from app.classes.data import Post, Comment, Feedback
from app.classes.forms import PostForm, CommentForm
from requests_oauth2.services import GoogleClient
from requests_oauth2 import OAuth2BearerToken
import requests
import datetime as dt
from bson import ObjectId


from newsapi import NewsApiClient

#Routing for the News Portion
@app.route('/newsFeed', methods=['GET', 'POST'])
def newsfeed():
    #Grabs Data from news API
    newsapi = NewsApiClient(api_key='6030a33d2e814654a43ce7aa2c368df7')
    top_headlines = newsapi.get_top_headlines(sources="cnn")

    articles = top_headlines['articles']

    news = []
    desc = []
    img = []
    #Saves the data in local variables (Maybe create classes to hold news in other file)
    for i in range(len(articles)):
        myarticles = articles[i]
        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])

    articleList = zip(news,desc,img)
    #Send the data to the html template
    #render the template
    return render_template("newsFeed.html", articleList = articleList)