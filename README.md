#Remove Saves

Remove all saved posts from specified subreddits that you are no longer interested in.

##Setup

1. You will need to have **praw** installed for the script to run properly. To add this library, run `pip install praw`. This may require you to start the terminal as administrator.
2. After signing into Reddit through your browser, go to *User Settings → Privacy & Security → App authorization → create another app...*. From here, copy the client ID and client secret for your new application.

	![settings](settings.PNG)

3. Open `removeSaves.py` and provide values to the variables on lines 8 through 11.
