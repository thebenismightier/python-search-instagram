import hmac
from instagram.client import InstagramAPI
from hashlib import sha256
from collections import OrderedDict
import sys

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

client_id = 'd2d0c7f8bc1a40a49be6efcef61dcc92'

api = InstagramAPI(client_id=client_id)

tag = input("Tag to look up: ")

all_media_ids = []
all_post_content = []
all_user_ids = []
all_user_data = []

result_media,junk = api.tag_recent_media(tag_name=tag, count=20)
for media in result_media:
    all_post_content.append(media.caption.text)
    all_user_ids.append(media.user.id)

print ("User information of 20 most recent posters:")
for user_id in all_user_ids:
    user = api.user(user_id)
    print (user.username + " : Posts=", str(user.counts['media']) +
           " Followers=" + str(user.counts['followed_by']) +
           " Follows=" + str(user.counts['follows']))
    
