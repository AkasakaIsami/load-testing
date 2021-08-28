import random
import time
import requests
import logging
from configparser import ConfigParser

from requests.models import Response
from utils import random_str, random_form_list
from login import _login
from create_and_start_conference import _get_all_users

cp = ConfigParser()
cp.read("config.ini")

base_address = cp.get("server", "base_address")

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

article_port = cp.get("server", "article_port")
meeting_port = cp.get("server", "meeting_port")
message_port = cp.get("server", "message_port")
pcmember_port = cp.get("server", "pcmember_port")
review_port = cp.get("server", "review_port")
user_port = cp.get("server", "user_port")

date = time.strftime("%Y-%m-%d", time.localtime())

def _get_user_by_username(username, token, headers= {}):
    url = f"{base_address}:{user_port}/user/findByUsername"
    headers["Authorization"] = "Bearer " + token
    params = {"username": username}
    r = requests.get(url=url, params=params, headers = headers)
    if r.status_code == 200:
        user = r.json()["responseBody"]["UserInformation"]
        logging.info(f"get user by username: {user}")
        #print(meetings)
        # logging.info(f"{username} get {len(meetings)} available meetings")
        return user
    else:
        logging.error(r)

def _get_available_meetings(username, token, headers = {}):
    url = f"{base_address}:{meeting_port}/user/availableMeeting"
    headers["Authorization"] = "Bearer " + token
    params = {"username": username}
    r = requests.get(url=url, params=params, headers = headers)
    if r.status_code == 200:
        meetings = r.json()["responseBody"]["meetings"]
        #print(meetings)
        logging.info(f"{username} get {len(meetings)} available meetings")
        return meetings
    else:
        logging.error(r)
    
    return None

def _submit_an_article(user, token, meeting, headers = {}):
    #logging.info(meeting)
    url = f"{base_address}:{article_port}/user/articleSubmission"
    headers["Authorization"] = "Bearer " + token
    authors = f"[{user}]"
    # print(authors)
    # authors.append(another_author)
    payload = {
        "meetingName": meeting["meetingName"],
        "username": user["username"],
        "essayTitle": random_str(),
        "essayAbstract": random_str(),
        "submitTime": date,
        "topic": meeting["topic"],
        "authors": authors,
    }

    file = {
        'essayPDF': open("test.pdf", "rb"),
        'Content-Disposition': 'form-data', 
        'Content-Type': 'application/pdf', 
        'filename':'test.pdf'
    }

    # logging.info(payload)
    r: Response = requests.post(url=url, data=payload, files=file, headers=headers)
    if r.status_code == 200:
        logging.info(f"{username} submit an article to meeting {meeting['meetingName']} success. Response: {r.text}")
    else:
        print(r.request)
        logging.error(r)



if __name__ == '__main__':
    usernames = ["test2", "test3"]
    username = random.choice(usernames)
    token = _login(username)
    user = _get_user_by_username(username, token)

    meetings = _get_available_meetings(username, token)

    # random choose a meeting to submit an article
    meeting = random.choice(meetings)
    logging.info(f"choose meeting {meeting['meetingName']}")
    
    # random choose another author
    all_users = _get_all_users(token)
    another_author = random.choice(all_users)
    while (another_author["username"] == username):
        another_author = random.choice(all_users)
    # submit an article
    _submit_an_article(user, token, meeting)
    


    
