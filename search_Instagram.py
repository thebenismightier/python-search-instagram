# Benny Ng
# bennyng@umich.edu
# 10/30/2015

import hmac
from textblob import TextBlob
from instagram.client import InstagramAPI
from hashlib import sha256
from collections import OrderedDict
import sys

class User:
    def __init__(self, id, name, num_followers, num_followed, num_posts):
        self.id = id
        self.name = name
        self.num_followers = num_followers
        self.num_followed = num_followed
        self.num_posts = num_posts
    
# For converting emoticons to empty characters
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

client_id = 'd2d0c7f8bc1a40a49be6efcef61dcc92'

# keep this global
api = InstagramAPI(client_id=client_id)

# Change the sensitivity to look for more 'emotional' posts. 
SUBJ_SENSITIVITY = 0.0 # between 0.0 and 1.0 (objective -> subjective)
POS_SENSITIVITY = 0.0 # polarity score float between [-1.0, 1.0]
NEG_SENSITIVITY = 0.0
all_media_ids = []
all_post_content = []
all_user_ids = []
all_user_data = []

def get_tagged_media(tag, get_more_posts):
    print("Getting tagged posts", end='')
    
    result_media, next_ = api.tag_recent_media(tag_name=tag)

    if get_more_posts == True:
        i = 0
        while next_ and i in range(9):
            i += 1
            result_media2, next_ = api.tag_recent_media(tag_name=tag, with_next_url=next_)
            print(".", end='')
            for media in result_media2:
                result_media.append(media)

    print()
    return result_media

def get_users_and_caption(result_media):
    print("Getting users and captions of posts")
    
    user_ids = []
    captions = []
    for media in result_media:
    # TODO: find a reasonable subj/pos/neg sensitivity
    # TODO: also consider the polarity of emojis
        post = media.caption.text.translate(non_bmp_map)
        captions.append(post)
        user_ids.append(media.user.id)
    return user_ids, captions

def get_sentiment_scores(captions):
    print("get_sentiment")
    # todo
    dict = {"positive": 0, "negative": 0, "neutral": 0}
    num_pos = 0
    num_neg = 0
    
    for caption in captions:
        post = TextBlob(caption)
        if post.sentiment.subjectivity > SUBJ_SENSITIVITY:
            if post.sentiment.polarity > POS_SENSITIVITY:
                dict["positive"] += 1
            elif post.sentiment.polarity < NEG_SENSITIVITY:
                dict["negative"] += 1
    dict["neutral"] = len(captions) - (dict["positive"] + dict["negative"])

    return dict

def get_user_data(user_ids):
    print("Getting user data")
    
    user_data = []
    for id in user_ids:
        user = api.user(id)
        user_data.append(User(id, user.username, user.counts['followed_by'], 
            user.counts['follows'], user.counts['media']))
    return user_data

def print_line_sep():
    print("===========================================\n")

def print_user_info(user_data):
    print_line_sep()
    print("User data of posters\n")
    print_line_sep()
    
    for user in user_data:
        print(user.name, ":", "Following(" + str(user.num_followed) + ")",
              "Followers(" + str(user.num_followers) + ")",
              "Posts(" + str(user.num_posts) + ")")
        
def print_sentiment_data(sentiments):
    print_line_sep()
    print("Post Sentiment Analysis")
    print_line_sep()
    
    print("Num Pos: " + str(sentiments["positive"]) +
      "\nNum Neg: " + str(sentiments["negative"]) +
      "\nNum Neutral: " + str(sentiments["neutral"]));

# Uncomment the input line to allow user to input other tags to analyze.
# otherwise, automatically searches for "CapitalOne"
def main():
    tag = "CapitalOne"
    # tag = input("Enter tag to search on Instagram: ")
    get_more_posts = True

    resp = input("Would you like to get more than 20 posts? Y/n ")
    if resp.upper() == "NO" or resp.upper() == "N":
        get_more_posts = False

    print("Hello, searching for", tag)
    result_media = get_tagged_media(tag, get_more_posts)
    user_ids, captions = get_users_and_caption(result_media)
    user_data = get_user_data(user_ids)
    sentiments = get_sentiment_scores(captions)
    
    print_user_info(user_data)
    print_sentiment_data(sentiments)

# Start
main()
