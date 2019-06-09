from tkinter import *
from tkinter import ttk
import sys
import os
import praw
from praw.models import Submission

USERNAME = ""
PASSWORD = ""
CLIENT_ID = ""
CLIENT_SECRET = ""
USER = praw.Reddit(user_agent='removeSaved', client_id=CLIENT_ID,  client_secret=CLIENT_SECRET, username=USERNAME, password=PASSWORD)

SUB_LIST_STRING = []
# List of posts
POSTS = []
# List of subreddits
SUBREDDITS = []
# Used to count number of posts from each subreddit
SUB_WITH_DUPES = []
# List of dicts with subreddits and correspoding counts
SUB_WITH_COUNT = []

def removeSub():
    global SUB_LIST_STRING
    index = 0
    searching = 1
    while (index < len(SUB_LIST_STRING) and searching):
        if save_listbox.get(ACTIVE) in SUB_LIST_STRING[index]:
            for item in POSTS:
                if isinstance(item, Submission):
                    if item.subreddit == save_listbox.get(ACTIVE)[:save_listbox.get(ACTIVE).find(" ")]:
                        item.unsave()
                else:
                    if item.submission.subreddit == save_listbox.get(ACTIVE)[:save_listbox.get(ACTIVE).find(" ")]:
                        item.unsave()
            searching = 0
            del SUB_LIST_STRING[index]
            save_listbox.delete(index)
        else:
            index += 1

def load_saves():
    global SUB_LIST_STRING
    global POSTS
    global SUBREDDITS
    global SUB_WITH_DUPES
    global SUB_WITH_COUNT

    SUB_LIST_STRING = []
    # List of posts
    POSTS = []
    # List of subreddits
    SUBREDDITS = []
    # Used to count number of posts from each subreddit
    SUB_WITH_DUPES = []
    # List of dicts with subreddits and correspoding counts
    SUB_WITH_COUNT = []
    COUNT = 0
    save_listbox.delete(0, END)
    save_listbox.pack()
    SAVED = USER.user.me().saved(limit=None)
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
        SUB_LIST_STRING.append(str(sub["name"]) + " " + str(sub["count"]))
    for sub in SUB_LIST_STRING:
        save_listbox.insert(END, sub)
    save_listbox.pack(fill=BOTH)

root = Tk()
root.title("SaveTools")

scrollbar = Scrollbar(root, orient="vertical")
save_listbox = Listbox(root, width=50, height=20, yscrollcommand=scrollbar.set)
scrollbar.config(command=save_listbox.yview)
scrollbar.pack(side="right", fill="y")
for sub in SUB_LIST_STRING:
    save_listbox.insert(END, sub)
save_listbox.pack(side="left",fill="both", expand=True)
load_button = Button(root, text="Load Saves", command=load_saves)
load_button.pack(side=BOTTOM, fill=BOTH)
remove_button = Button(root, text="Remove", command=removeSub)
remove_button.pack(side=TOP, fill=BOTH)
password_entry = Entry(root)
password_entry.pack(side=BOTTOM)
hint_password = Label(root, text="Password")
hint_password.pack(side=BOTTOM)
username_entry = Entry(root)
username_entry.pack(side=BOTTOM)
hint_username = Label(root, text="Username")
hint_username.pack(side=BOTTOM)
root.mainloop()
