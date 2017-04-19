#!/bin/python

import os
import shutil
import pickle
import argparse

import praw

'''
saved-parser parses and organizes your reddit saved content

Usage: 
    - Fill out the dict in catagories-stub.py
      Each key is a different catagory. The value is 
      a list of subreddits belonging to that catagory.

    - Run catagories-stub.py, it will store the dict in a file

    - Run saved-parser.py, it will load the catagories dict and 
      use it to organize your saved content

    - For each catagory, saved-parser will create a file of the same name
      with a entry for each saved item belonging to that catagory.     
'''

DIVIDER = '-' * 30
OUTPUT_DIR = 'output'
CATAGORIES_FILE = 'catagories.pickle'
OTHER_FILE = 'other'                    # all content not falling in any catagory will be stored in a file OTHER_FILE

USER_AGENT = 'saved-parser'


arg_parser = argparse.ArgumentParser(description='Organizes and parses your saved content')
arg_parser.add_argument('--client-id', type=str, required=True)
arg_parser.add_argument('--client-secret', type=str, required=True)
arg_parser.add_argument('--username', type=str, required=True)
arg_parser.add_argument('--password', type=str, required=True)
arg_parser.add_argument('--unsave', type=bool, required=False, default=False)

args = arg_parser.parse_args()


saved = praw.Reddit(client_id=args.client_id,
                    client_secret=args.client_secret,
                    user_agent=USER_AGENT,
                    username=args.username,
                    password=args.password).user.me().saved(limit=None)


class SavedItem:

    def __init__(self, link, url, title, subreddit):
        self.link = link
        self.url = url
        self.title = title
        self.subreddit = subreddit

    def __str__(self):
        return f'Title: {self.title}\nSubreddit: {self.subreddit}\nUrl: {self.url}\nLink: {self.link}\n'



# Load catagories dict
catagories = {}
with open(CATAGORIES_FILE, 'rb') as fh:
    catagories = pickle.load(fh)


# Create the output dir - delete it and all contents if it exists
if os.path.exists(OUTPUT_DIR):
    shutil.rmtree(OUTPUT_DIR)

os.makedirs(OUTPUT_DIR)


for reddit_content in saved:
    # Pull info from reddit_content
    link = reddit_content.shortlink if type(reddit_content) is praw.models.Submission else reddit_content.permalink()
    url = reddit_content.url if type(reddit_content) is praw.models.Submission else reddit_content.submission.url 
    title = reddit_content.title if type(reddit_content) is praw.models.Submission else reddit_content.submission.title
    subreddit = str(reddit_content.subreddit).lower()

    saved_item = SavedItem(link, url, title, subreddit)

    if args.unsave:
        saved_item.unsave()

    found = False

    for catagory, catagory_subreddits in catagories.items():
        # Open the file for this catagory
        with open(os.path.join(OUTPUT_DIR, catagory), 'a+') as fh:
            # Compare the subreddit of the current reddit_content against each subreddit in the catagory
            for catagory_subreddit in catagory_subreddits:
                if saved_item.subreddit == catagory_subreddit.lower():
                    print(saved_item, file=fh)
                    print(DIVIDER, file=fh)
                    found = True

    if not found:
        with open(os.path.join(OUTPUT_DIR, OTHER_FILE), 'a+') as fh:
            print(saved_item, file=fh)
            print(DIVIDER, file=fh)
