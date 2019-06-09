""" Script used to remove posts from specified subreddits from a user's saved posts. """
import sys
import os
import praw
from praw.models import Submission

# Replace username, password, client_id, and client_secret
USERNAME = ""
PASSWORD = ""
CLIENT_ID = ""
CLIENT_SECRET = ""

USER = praw.Reddit(user_agent='removeSaved', client_id=CLIENT_ID, client_secret=CLIENT_SECRET, username=USERNAME, password=PASSWORD)
# List of posts
POSTS = []
# List of subreddits
SUBREDDITS = []
# Used to count number of posts from each subreddit
SUB_WITH_DUPES = []
# List of dicts with subreddits and correspoding counts
SUB_WITH_COUNT = []
SAVED = USER.user.me().saved(limit=None)
COUNT = 0
print('Please wait as your saved posts are loaded. This may take a while.')

for item in SAVED:
    if isinstance(item, Submission):
        if item.subreddit not in SUBREDDITS:
            SUBREDDITS.append(item.subreddit)
            COUNT += 1
        SUB_WITH_DUPES.append(item.subreddit)
    else:
        if item.submission.subreddit not in SUBREDDITS:
            SUBREDDITS.append(item.submission.subreddit)
            COUNT += 1
        SUB_WITH_DUPES.append(item.submission.subreddit)
    POSTS.append(item)

# Create an array of dicts containing subreddit names with the number of saved posts
INDEX = 0
while INDEX < COUNT:
    SUB_WITH_COUNT.append({"name":SUBREDDITS[INDEX], "count":0})
    INDEX += 1

# Determine the number of posts for each subreddit
for sub in SUB_WITH_DUPES:
    for sub2 in SUB_WITH_COUNT:
        if sub2["name"] == sub:
            sub2["count"] += 1

# Sort subreddits in descending order of number of saved posts
SUB_WITH_COUNT = sorted(SUB_WITH_COUNT, key=lambda count: float(count['count']), reverse=True)

# Print out updated SUB_WITH_COUNT
for sub in SUB_WITH_COUNT:
    print(sub["name"], str(sub["count"]))

def remove_saved(COUNT):
    """ Removes posts from user inputed subreddit and calls itself at the end in case\
     posts from another subreddit should be removed. """
    posts_removed = 0
    if COUNT > 0:
        sub_to_remove = prompt_user()
        # Find total number of posts from subreddit the user inputted
        for sub2 in SUB_WITH_COUNT:
            if sub2["name"] == sub_to_remove:
                COUNT = sub2["count"]
        for item in POSTS:
            if isinstance(item, Submission):
                if item.subreddit == sub_to_remove:
                    #print(item.title + "\n▓" + item.permalink)
                    item.unsave()
                    posts_removed += 1
                    show_progress(float(posts_removed)/COUNT)
            else:
                if item.submission.subreddit == sub_to_remove:
                    #print(item.submission.title + "\n▓" + item.permalink)
                    item.unsave()
                    posts_removed += 1
                    show_progress(float(posts_removed)/COUNT)
        print(" Complete")
        if input("Go again?(y/n)") == "y":
            SUBREDDITS.remove(sub_to_remove)
            remove_saved(COUNT)
    else:
        print("Nothing to remove")

def prompt_user():
    """ Asks user for a subreddit until one that is in the saved list is entered. """
    sub_to_remove = input("Subreddit to remove: ")
    if sub_to_remove not in SUBREDDITS:
        print("There are no posts from", sub_to_remove, "to remove.")
        prompt_user()
    else:
        return sub_to_remove

def show_progress(val):
    ''' Show the progress of removing posts. '''
    if val < 0.1:
        sys.stdout.write("\r░░░░░░░░░░")
    elif val < 0.2:
        sys.stdout.write("\r▓░░░░░░░░░")
    elif val < 0.3:
        sys.stdout.write("\r▓▓░░░░░░░░")
    elif val < 0.4:
        sys.stdout.write("\r▓▓▓░░░░░░░")
    elif val < 0.5:
        sys.stdout.write("\r▓▓▓▓░░░░░░")
    elif val < 0.6:
        sys.stdout.write("\r▓▓▓▓▓░░░░░")
    elif val < 0.7:
        sys.stdout.write("\r▓▓▓▓▓▓░░░░")
    elif val < 0.8:
        sys.stdout.write("\r▓▓▓▓▓▓▓░░░")
    elif val < 0.9:
        sys.stdout.write("\r▓▓▓▓▓▓▓▓░░")
    elif val < 1:
        sys.stdout.write("\r▓▓▓▓▓▓▓▓▓░")
    elif val == 1:
        sys.stdout.write("\r▓▓▓▓▓▓▓▓▓▓")
    sys.stdout.flush()
remove_saved(COUNT)
