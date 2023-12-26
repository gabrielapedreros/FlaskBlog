"""Forms: Handles users who are liking/disliking a post"""
from flask_wtf import FlaskForm
#define web forms as a python class
from wtforms import SubmitField
#validates forms
class LikeForm(FlaskForm):
    """If post liked"""
    submit = SubmitField('Like')
class DislikeForm(FlaskForm):
    """if post disliked"""
    submit = SubmitField('Dislike')
