# Gabriela Pedreros - gp21j
""" This file defines route handlers for the Flask app """
import os
from urllib.parse import quote_plus, urlencode    #encode url, key-value pairs
from flask import render_template, jsonify, session, redirect, url_for, flash
#including flask web app components ^
from flask_login import login_user, logout_user, current_user, login_required
#to handle user authentication ^
from flaskblog import app, db, oauth                #import flask app
from flaskblog.models import NewsItem, User, NewsItemLike    #import models
from flaskblog.hackernews import fetch_hackernews_top_stories    #import hackernews
from flaskblog.forms import LikeForm, DislikeForm            #import forms   

@app.route('/')
def home():
    """ Home page route handler """
    fetch_hackernews_top_stories()        # fetch and update the database with the latest stories
    news_items = NewsItem.query.all()    # fetch all news items from database

    # fill out forms for each news item
    like_forms = {item.id: LikeForm(prefix=str(item.id)) for item in news_items}
    dislike_forms = {item.id: DislikeForm(prefix=str(item.id)) for item in news_items}

    likes_counts = {                # count likes for each item
        item.id: NewsItemLike.query
        .filter_by(news_item_id=item.id, like=True)
        .count()
        for item in news_items
    }
    dislikes_counts = {            # count dislikes for each item
        item.id: NewsItemLike.query
        .filter_by(news_item_id=item.id, like=False)
        .count()
        for item in news_items
    }
    for item in news_items:    # convert time to integer if string
        if isinstance(item.time, str):
            try:
                item.time = int(item.time)
            except ValueError:
                item.time = 0  
    #sort news items by number of likes and then by time 
    news_items = sorted(
        news_items,
        key=lambda item: (likes_counts[item.id], item.time),
        reverse=True
    )
    #template of what will be displayed on the home page
    return render_template(    #sends home.html to broswer
        'home.html',
        news_items=news_items,
        likes_counts=likes_counts,
        dislikes_counts=dislikes_counts,
        like_forms=like_forms,
        dislike_forms=dislike_forms
    )

@app.route('/about')
def about():
    """ About page route handler """
    return render_template('about.html', title='About')    #send about.html to browser
    
@app.route('/newsfeed')
def newsfeed():
    """ Newsfeed page route handler which returns news items in JSON format """
    fetch_hackernews_top_stories()  
    news_items = NewsItem.query.all()
    return jsonify(
        [
                {
                    'by': item.by,
                    'descendants': item.descendants,
                    'id': item.id,
                    'kids': item.kids,
                    'score': item.score,
                    'text': item.text,
                    'time': item.time,
                    'title': item.title,
                    'type': item.type,
                    'url': item.url
                } for item in news_items
        ]
    )
    
@app.route("/login")
def login():
    """ Login page route handler """
    return oauth.auth0.authorize_redirect(    #when user login, use auth0
        redirect_uri=url_for("callback", _external=True)
    )
    
@app.route("/callback", methods=["GET", "POST"])
def callback():
    """ This route handles the redirection to the home page once the user has been authenticated """
    #when user logs in/out, redirection
    userinfo = oauth.auth0.get(f'https://{os.environ.get("AUTH0_DOMAIN")}/userinfo').json()
    auth0_user_id = userinfo['sub']
    username = userinfo.get('nickname', userinfo['name'])
    email = userinfo.get('email')
    user = User.query.filter_by(auth0_user_id=auth0_user_id).first()
    if not user:
        user = User(auth0_user_id=auth0_user_id, username=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user)
    return redirect(url_for('home'))
    
@app.route("/logout")
def logout():
    """ This route handles the redirections to the logout page for user from the website"""
    logout_user()
    session.clear()
    return redirect(
        "https://" + os.environ.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": os.environ.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )
    
@app.route('/like/<int:news_item_id>', methods=['POST'])
@login_required
def like_news_item(news_item_id):
    """ This route handles when a news item is liked by a user. This route responds
        to POST requests """
    form = LikeForm()    #call like forms when there is a submission
    if form.validate_on_submit():    #valid form/submission
        existing_like = NewsItemLike.query.filter_by(
            user_id=current_user.id,
            news_item_id=news_item_id).first()
        if existing_like:
            if existing_like.like:
                db.session.delete(existing_like)    #delete existing like if already liked (unliking)
            else:
                existing_like.like = True            #create like if none exists
                db.session.commit()
        else:
            new_like = NewsItemLike(user_id=current_user.id, news_item_id=news_item_id, like=True)
            db.session.add(new_like)
            db.session.commit()
    return redirect(url_for('home'))
    
@app.route('/dislike/<int:news_item_id>', methods=['POST'])
@login_required
def dislike_news_item(news_item_id):
    """ This route handles when a news item is disliked by a user. This route responds
        to POST requests """
    form = DislikeForm()    #call dislike form when there is a submission
    if form.validate_on_submit():
        existing_like = NewsItemLike.query.filter_by(
            user_id=current_user.id,
            news_item_id=news_item_id
        ).first()
        if existing_like:
            if not existing_like.like:    #remove existing dislike (undisliking)
                db.session.delete(existing_like)
            else:
                existing_like.like = False    #create dislike if none exist
                db.session.commit()
        else:
            new_like = NewsItemLike(user_id=current_user.id, news_item_id=news_item_id, like=False)
            db.session.add(new_like)
            db.session.commit()
    return redirect(url_for('home'))

@app.route('/profile')
@login_required
def profile():
    """profile information"""
    return render_template('profile.html', title='Profile') #sends profile.html to browser

@app.route("/admin")
@login_required
def admin():
    """ Route handler for admin page """
    # retrieve news items and users from database
    news_items = NewsItem.query.all()       
    users = User.query.all()  

    user_interactions = {            #sets information of interaction 
        news.id: NewsItemLike.query
        .filter_by(news_item_id=news.id).all()
        for news in news_items
    }
    return render_template(            #sends admin.html to browser
        "admin.html",
        users=users,news_items=news_items,
        user_interactions=user_interactions
    )

@app.route("/admin/delete-user/<int:user_id>", methods=['POST'])
@login_required
def delete_user(user_id):
    """ Route handler for deleting a user from the website"""
    user = User.query.get_or_404(user_id)

    #delete likes/dislikes associated with the user
    NewsItemLike.query.filter_by(user_id=user_id).delete()
    db.session.delete(user)                # delete the user
    db.session.commit()                    # commit changes to the database

    flash("User and associated likes/dislikes deleted successfully.", "success")
    return redirect(url_for('admin'))
