from sensitive import client_id
from sensitive import client_secret
from sensitive import user_agent
import praw
import pytesseract
import re
import io
import requests

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


try:
    from PIL import Image
except ImportError:
    import Image

# reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
# subreddit = reddit.subreddit("wallstreebets")
#
# comment_stream = subreddit.stream.comments(pause_after=-1, skip_existing=True)
# submission_stream = subreddit.stream.submissions(pause_after=-1, skip_existing=True)

comment_counter = 0
submission_counter = 0


def Find(string):
    # findall() has been used
    # with valid conditions for urls in string
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s(" \
            r")<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’])) "
    url = re.findall(regex, string)
    return [x[0] for x in url]


# while True:
#     for comment in comment_stream:
#         comment_counter += 1
#         if comment is None:
#             break
#         print("Comment #%s /n" % comment_counter, comment.body)
#     for submission in submission_stream:
#         submission_counter += 1
#         if submission is None:
#             break
#         print("Submission #%s /n" % submission_counter, submission.title, " ", submission.selftext)
#         url_list = Find(submission.selftext)
#         image_list = []
#         if len(url_list) != 0:
#             for url in url_list:
#                 if ["jpg", "png"] in url:
#                     response = requests.get(url)
#                     img = Image.open(io.BytesIO(response.content))
#                     text = pytesseract.image_to_string(img)
#                     print("IMAGE TEXT: ", text)

def GrabText(url):
    if ("png" in url) or ("jpg" in url):
        response = requests.get(url)
        img = Image.open(io.BytesIO(response.content))
        text = pytesseract.image_to_string(img)
        return text


print("IMAGE TEXT: ", GrabText("https://preview.redd.it/c4yn7w22ut871.png?width=1904&format=png&auto=webp&s=6ba97b42ef50a82a7ac6d3509bc3fa4e3f417687"))
