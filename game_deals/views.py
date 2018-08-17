from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Deal

# Create your views here.

#! usr/bin/env python3
import praw
import pandas as pd
import datetime as dt
import openpyxl
import re

from .keys import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, IGDB_KEY, REDDIT_PW, REDDIT_USER


reddit = praw.Reddit(client_id = REDDIT_CLIENT_ID,
                     client_secret = REDDIT_CLIENT_SECRET, 
                     user_agent = 'scrappy', 
                     username = REDDIT_USER, 
                     password = REDDIT_PW)


def parse_title(title):
    price = re.search('[£$€]\d+(?:\.\d{2})?', title)
    discount = re.search('\d+%', title)
    name = re.search('(?<=\])(.*)', title)

    if not price:
        price = "N/A"
    else:
        price = price.group()
    if not discount:
        discount = "N/A"
    else:
        discount = discount.group()
    if not name:
        name = title
    else:
        name = name.group()

    return name, price, discount
    

def get_date(created):
    return dt.datetime.fromtimestamp(created)


def clean_text(rgx_list, text):
    new_text = text
    for rgx_match in rgx_list:
        new_text = re.sub(rgx_match, '', new_text)
    return new_text


def make_deal(game, submission, store):
    deal = Deal()
    
    title, price, discount = parse_title(game)

    rep = {"Daily Deal:": "", "Daily Deal - ": "","Daily Deal": ""}
    # use these three lines to do the replacement
    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    title = pattern.sub(lambda m: rep[re.escape(m.group(0))], title)

    # Remove all currency values, discount percentages and strings within brackets
    regex = ['[£$€]\d+(?:\.\d{2})?','\d+%','\(.*\)']
    title = clean_text(regex, title)

    # Check to see if there are any games in the db with the same title
    deals = Deal.objects.filter(game = title)
    # If not, then call the igdb api
    if not deals.count():
        print("Game not in db, calling IGDB api..")
        igdb_result = get_cover_art(title)
        cover_image_hash = ""
        for game in igdb_result.body:
            try:
                cover_image_hash = game['cover']['cloudinary_id']
                print("Obtained cover, brother")
                break
            except Exception:
                print("No cover today, brother")
                pass
        deal.cover_hash = cover_image_hash
        
        print(igdb_result.body)
    else:
        print("Game already in db")
        

    # Set deal attr and insert it into db
    deal.game = title
    deal.price = price
    deal.store = store 
    deal.discount = discount 
    deal.link = submission.url
    deal.pub_date = get_date(submission.created)     
    deal.save()


def get_deals():
    game_deals = reddit.subreddit('GameDeals')
    new_game_deals = game_deals.new(limit=50)

    for submission in new_game_deals:
        store = re.search('(?<=\[)(.*?)(?=\])', submission.title).group()
        title, price, discount = parse_title(submission.title)

        if len(title.split('|')) > 1:
            for game in title.split('|'):
                make_deal(game, submission, store)
                pass
        elif len(title.split(',')) > 1:
            for game in title.split(','):
                make_deal(game, submission, store)
                pass
        else:
            make_deal(submission.title, submission, store)     


def get_cover_art(game):
    ig_db = igdb(IGDB_KEY)
    result = ig_db.games({
        'search': game,
        'fields': ['cover','name']
    })
    return result


def index(request):
    get_deals()
    latest_game_deals = Deal.objects.order_by('-pub_date')[:10]
    template = loader.get_template('game_deals/index.html')
    context = {
        'latest_game_deals': latest_game_deals,
    }
    return HttpResponse(template.render(context, request))