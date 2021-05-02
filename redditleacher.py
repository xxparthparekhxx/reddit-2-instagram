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
            "Reddit_client_id": input("enter your reddit_client_id :"),
            "Reddit_client_secret": input("enter your reddit client secret :"),
            "Instagram_id": input("enter your Insragram id #locally stored :"),
            "Instagam_password": input("enter your Instagram password :"),
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

    number_of_posts = int(
        input("enter the number of posts you want to make :")
    )  # gets number of posts to be make

    Tags = input("paste in the #tags in here you want on your posts with :")


    root = make_download_folder()

    # downloading images

    i = 0
    arr = ["jpg"]
    for submission in reddit.subreddit(substr).hot(limit=number_of_posts):
        url = submission.url
        response = requests.get(url)
        ext = str(url[-3:])
        if ext in arr:
            i += 1
            with open('captions.txt',"a") as f:
                f.write(str(submission.title)+"\n")
            f.close()
            with open("{}".format(i) + ".{}".format("jpg"), "wb") as f:
                f.write(response.content)
            print("download {} completed!".format(i))
            time.sleep(2)

    for img in os.listdir():
        try:
            image = Image.open(img)
            print(image.size)
            resized_image = image.resize((1080,1080))
            resized_image.save('{}'.format(img))
        except:
            pass
    
    #posting of the images starts here
    with open("captions.txt","r") as f:
        captions = f.readlines()
    print(captions)
    i=1
    while i <= len(captions):
        try:
          caps = captions[i]+ Tags
          bot.upload_photo("{}.jpg".format(i+1),caps)
        except:
          i +=1
          caps = captions[i]+ Tags
          bot.upload_photo("{}.jpg".format(i+1) , caps)
        i += 1
        if i+1 != number_of_posts:
            time.sleep(random.randrange(3600,7200))
    

