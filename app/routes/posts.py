# Posts are a general feture that allows a user to post a comment.  Posts are associated with 
# comments.  Comments are comments on Posts.  It is a discussion board sort of relationship.
# In this site, Posts are associated with Feedback. Posts are posts on Feedback records and serve
# to start a conversation about the feedback record. 

# For a thorough description of this sort of code works, see the Feedback.py file which has
# thorough comments.

from app import app
from flask import render_template, redirect, url_for, request, session, flash
from app.classes.data import Post, Comment, Feedback
from app.classes.forms import PostForm, CommentForm
from requests_oauth2.services import GoogleClient
from requests_oauth2 import OAuth2BearerToken
import requests
import datetime as dt
from bson import ObjectId

@app.route('/posts')
def posts():
 
    posts = Post.objects()
    return render_template("posts.html", posts=posts)

@app.route('/post/<postId>')
def post(postId):
  
    post = Post.objects.get(pk=postId)
    comments = Comment.objects(post=postId)
    return render_template('post.html',post=post,comments=comments)

@app.route('/newcomment/<postId>', methods=['GET', 'POST'])
def newcomment(postId):
   
    form=CommentForm()
    post=Post.objects.get(pk=postId)
    if form.validate_on_submit():
        newComment = Comment(
            comment=form.comment.data, 
            user=ObjectId(session['currUserId']),
            post=post.id
        )
        newComment.save()
        newComment.reload()
        return redirect('/post/'+postId)
    return render_template('commentform.html',post=post, form=form)

@app.route('/deletecomment/<postId>/<commentId>')
def deletecomment(postId, commentId):
 
    deleteComment=Comment.objects.get(pk=commentId)
    if str(deleteComment.user.id) == session['currUserId']:
        deleteComment.delete()
        flash('Comment deleted.')
    else:
        flash("You can't delete the comment because you don't own it.")
    return redirect('/post/'+postId)

@app.route('/feedbackpost/<feedbackid>', methods=['GET', 'POST'])
@app.route('/jobq/<jobid>', methods=['GET', 'POST'])
@app.route('/newpost', methods=['GET', 'POST'])
def newpost(jobid="none",feedbackid="none"):

    form = PostForm()

    if not jobid == "none":
        postJob = Job.objects.get(pk=jobid)
    else:
        postJob = None
    if not feedbackid == "none":
        feedbackJob = Feedback.objects.get(pk=feedbackid)
    else:
        feedbackJob = None

    if form.validate_on_submit():
        newPost = Post(
            subject=form.subject.data, 
            body=form.body.data, 
            user=ObjectId(session['currUserId'])
        )
        newPost.save()
        newPost.reload()

        if not jobid == 'none':
            newPost.update(job = ObjectId(jobid))
        if not feedbackid == 'none':
            newPost.update(feedback = ObjectId(feedbackid))

        return render_template('post.html',post=newPost, job=postJob, feedback=feedbackJob)

    flash('Fill out the form to create a new post')
    return render_template('postform.html', form=form, job=postJob, feedback=feedbackJob)

@app.route('/editpost/<postId>', methods=['GET', 'POST'])
def editpost(postId):

    editPost = Post.objects.get(pk=postId)
    if str(editPost.user.id) == session['currUserId']:
        form = PostForm()
        if form.validate_on_submit():
            editPost.update(
                subject=form.subject.data,
                body=form.body.data,
                modifydate=dt.datetime.utcnow()
            )
            editPost.reload()
            flash('The post has been edited.')
            return render_template('post.html', post=editPost)
        flash('Change the fields below to edit your post')
        form.subject.data = editPost.subject
        form.body.data = editPost.body

        return render_template('postform.html', form=form)
    else:
        flash("You can't edit this post because you are not the author.")
        return redirect('/post/'+postId)

@app.route('/deletepost/<postId>')
def deletepost(postId):

    deletePost = Post.objects.get(pk=postId)
    if str(deletePost.user.id) == session['currUserId']:
        deletePost.delete()
        flash('Post was deleted')
        posts=Post.objects()
        return render_template('posts.html',posts=posts)
    else:
        flash("You can't delete this post because you are not the author")
        return redirect('/post/'+postId)