# Copyright (c) 2015–2016 Molly White
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import tweepy
import json
from stuffs import *
from time import gmtime, strftime

import get_data

# ====== Individual bot configuration ==========================
bot_username = 'Creature Wise'
logfile_name = bot_username + ".log"

# ==============================================================

# Twitter authentication
auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
api = tweepy.API(auth)



class MyStreamListener(tweepy.StreamListener):

    def on_data(self, data):
        
        try:
            status = json.loads(data)
            screen_name = status["user"]["screen_name"]

            status_content = status["text"].replace("@CreatureWise", "")

            #Use google API to get the location finformation
            lon, lat, place = get_data.get_location(status_content)

            new_id = tweet_text(place, screen_name, status["id"], lat, lon)

            # Find animal information + tweet it
            tweet_media(lon, lat, screen_name, status["id"])
        except tweepy.error.TweepError as e:
             log(e.message)
        except:
            pass
            # api.update_stat us("@%s Sorry, an error has occured"%(screen_name), in_reply_to_status_id = status["id"])

        return True

    def on_error(self, status):
        print status



def listen():
    myStreamListener = MyStreamListener()

    myStream = tweepy.Stream(api.auth, myStreamListener)

    myStream.filter(track=['@CreatureWise'], async=True)


def tweet_text(description, screen_name, tweet_id, lat, lon):
    """Send out the text as a tweet."""

   
    text = "@%s Finding animals near %s"%( screen_name, description)

    if len(text) > 140:
        text = "@%s can you find a %s? There are %s species nearby, %s"%( screen_name, name,num_animals, url )

    # Send the tweet and log success or failure
    try:
        status = api.update_status(text, in_reply_to_status_id = tweet_id, lat = lat, lon = lon)
    #     # print myStream.filter(track=['@CreatureWise'], async=True)
    except tweepy.error.TweepError as e:
        print e.message
        log(e.message)
    else:
        log("Tweeted: " + text)


    return status.id_str



def tweet_media(lon, lat, screen_name, tweet_id):
    """Send out the text as a tweet."""

    # Get the data we are going to send
    lsid, name, science_name, url, image_loc, num_animals = get_data.get_animal(lon, lat)
    print "Got animal information"

    text = "@%s can you find a %s (%s)? There are %s species nearby, %s"%( screen_name, name, science_name,num_animals, url )

    if len(text) > 140:
        text = "@%s can you find a %s?  There are %s species nearby, %s"%( screen_name, name,num_animals, url )

    # Send the tweet and log success or failure
    try:
        api.update_with_media(image_loc, status=text, in_reply_to_status_id = tweet_id, lat = lat, lon = lon)
    except tweepy.error.TweepError as e:
        print e.message
        log(e.message)
    else:
        log("Tweeted: " + text)


def log(message):
    """Log message to logfile."""
    path = os.path.realpath(os.getcwd())
    with open(os.path.join(path, logfile_name), 'a+') as f:
        t = strftime("%d %b %Y %H:%M:%S", gmtime())
        f.write("\n" + t + " " + message)


if __name__ == "__main__":

    # lon, lat, place = get_data.get_location(" Monterey")
    # print lon, lat, place
    listen()

    # log("msg")
