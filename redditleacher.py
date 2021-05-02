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


def getcredentials():
    if "creds.json" not in os.listdir():
        print("First time setup! \n enter your credentials below")
        credentials = {
            "Reddit_client_id": input("enter your reddit_client_id"),
            "Reddit_client_secret": input("enter your reddit client secret"),
            "Instagram_id": input("enter your Insragram id #locally stored"),
            "Instagam_password": input("enter your Instagram password"),
        }
        with open("creds.json", "w") as f:
            json.dump(credentials, f)
        return credentials
    elif "creds.json" in os.listdir():
        print("retriving credentials")
        with open("creds.json", "r") as f:
            credentials = json.load(f)
        return credentials

def make_download_folder():
    root = os.getcwd()

    if "downloadsdir" not in os.listdir():
        downloads = os.getcwd()+"\\downloadsdir"
        os.mkdir(downloads)
    elif "downloadsdir" in os.listdir():
        os.chdir("downloadsdir")
        for ele in os.listdir():
            os.remove(ele)
    return root
        
if __name__ == "__main__":

    credentials = getcredentials()

    reddit = reddit_initializer(
        credentials.get("Reddit_client_id"), credentials.get("Reddit_client_secret")
    )

    bot = Bot() # insragram logging in
    bot.login(
        username=credentials.get("Instagram_id"),
        password=credentials.get("Instagam_password"),
    )

    substr = input(
        "enter the subreddit you want to get your post from r/"
    )  # gets subreddit from user

    

