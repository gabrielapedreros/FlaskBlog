# Gabriela Pedreros - gp21j
""" This file will request information from the Hacker news portal and store it in the database. """
import requests                        #make http requests
from flaskblog.models import NewsItem  #use NewItem from models database
from flaskblog import db                #use database
def fetch_hackernews_top_stories():
    """ fetch data from hacker news by performing http get request to Hacker News API endpoint """
    response = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty")
    top_story_ids = response.json()[:30]  #fetch 30 stories & convert from JSON to list/dict 
    for story_id in top_story_ids:
        if NewsItem.query.get(story_id) is not None:    # check if the story exists
            continue
        story_response = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json?print=pretty")
        story_data = story_response.json()
        # storing values in db, ensuring no null values
        news_item = NewsItem(
            id=story_data['id'],
            by=story_data.get('by', ''),
            descendants=story_data.get('descendants', 0),
            kids=str(story_data.get('kids', [])),
            score=story_data.get('score', 0),
            text=story_data.get('text', ''),
            time=story_data.get('time', 0),
            title=story_data.get('title', 'No Title'),
            type=story_data.get('type', ''),
            url=story_data.get('url', '')
        )
        db.session.add(news_item)
    db.session.commit()    #commit to db
