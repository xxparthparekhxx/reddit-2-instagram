import praw, requests, os, shutil, time, pathlib, random, glob, json,PIL
from instabot import Bot
from PIL import Image

def reddit_initializer(Client_Id, Client_Secret):
    reddit = praw.Reddit(
        client_id=Client_Id,
        client_secret=Client_Secret,
        user_agent="bot 0.1",
    )
    print("reddit is ready?..." + str(reddit.read_only))
    return reddit
