# Gabriela Pedreros - gp21j
""" Define forms for Flask web app using Flask WTF and WTForms, which handle user interactions """
from flask_wtf import FlaskForm    #define web forms to handle form submissions
from wtforms import SubmitField    #define button for submissions
class LikeForm(FlaskForm):
    """ If news post is liked by user, use this form """
    submit = SubmitField('Like')
class DislikeForm(FlaskForm):
    """ If news post is disliked by user, use this form """
    submit = SubmitField('Dislike')
