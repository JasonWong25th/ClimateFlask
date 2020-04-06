from app import app
from flask import render_template, redirect, url_for, request, session, flash
from app.classes.data import Post, Comment, Feedback
from app.classes.forms import PostForm, CommentForm
from requests_oauth2.services import GoogleClient
from requests_oauth2 import OAuth2BearerToken
import requests
import datetime as dt
from bson import ObjectId

import json

from newsapi import NewsApiClient

#Routing for the News Portion
@app.route('/newsFeed', methods=['GET', 'POST'])
def newsfeed():
    url = ('http://newsapi.org/v2/everything?'
       'q=climate&'
       'sortBy=relevancy&'
       'apiKey=6030a33d2e814654a43ce7aa2c368df7')
    #Grabs Data from news API
    rawResponses = requests.get(url).json()


    news = []
    desc = []
    img = []

    if(rawResponses['status'] == "ok"):
        for i in range(len(rawResponses['articles'])):
            myarticle = rawResponses['articles'][i]
            news.append(myarticle['title'])
            desc.append(myarticle['description'])
            img.append(myarticle['urlToImage'])


    '''
    news_json = json.loads()

    news = []
    desc = []
    img = []

    if(rawResponses[1] == "ok"):
        for i in rawResponses['totalResults']:
            myarticle = rawResponses['articles']
            news.append(myarticle['title'])
            desc.append(myarticle['description'])
            img.append(myarticle['urlToImage'])


    
    newsapi = NewsApiClient(api_key='6030a33d2e814654a43ce7aa2c368df7')
    top_headlines = newsapi.get_everything(sources="national-geographic")

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
    '''
    articleList = zip(news,desc,img)
    return render_template("newsFeed.html", articleList = articleList)