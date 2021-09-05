import random
import time
import requests
import logging
from configparser import ConfigParser
from requests.api import head

from requests.models import Response
from utils import random_str, random_form_list
from login import _login
from create_and_start_conference import _begin_reivew

cp = ConfigParser()
cp.read("config.ini")

base_address = cp.get("server", "base_address")

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

user_auth_port = cp.get("server", "user_auth_port")
author_article_port = cp.get("server", "author_article_port")
admin_meeting_port = cp.get("server", "admin_meeting_port")
pcmember_port = cp.get("server", "pcmember_port")
chair_port = cp.get("server", "chair_port")
notice_port = cp.get("server", "notice_port")

date = time.strftime("%Y-%m-%d", time.localtime())

def _get_user_by_username(username, token, headers= {}):
    url = f"{base_address}:{user_auth_port}/user/username"
    headers["Authorization"] = "Bearer " + token
    params = {"username": username}
    r = requests.get(url=url, params=params, headers = headers)
    if r.status_code == 200:
        user = r.json()
        logging.info(f"get user by username: {user}")
        #print(meetings)
        # logging.info(f"{username} get {len(meetings)} available meetings")
        return user
    else:
        logging.error(f"get user by username fail, {r.status_code}, {r.text}")
        exit()

def _get_available_meetings(username, token, headers = {}):
    url = f"{base_address}:{user_auth_port}/user/availableMeeting"
    headers["Authorization"] = "Bearer " + token
    params = {"username": username}
    r = requests.get(url=url, params=params, headers = headers)
    if r.status_code == 200:
        meetings = r.json()["responseBody"]["meetings"]
        #print(meetings)
        logging.info(f"{username} get {len(meetings)} available meetings")
        return meetings
    else:
        logging.error(f"{username} get available meetings failed, {r.status_code}, {r.text}")
    
    return None

def _submit_an_article(user, token, meeting, headers = {}):
    #logging.info(meeting)
    url = f"{base_address}:{author_article_port}/user/articleSubmission"
    headers["Authorization"] = "Bearer " + token
    author = {
        "fullname": user["fullname"],
        "institution": user["institution"],
        "region": user["region"],
        "email": user["email"]
    }
    authors = f"[{author}]"
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
        logging.info(f"{user['username']} submit an article to meeting {meeting['meetingName']} success. Response: {r.text}")
    else:
        logging.error(f"{user['username']} submit an article to meeting {meeting['meetingName']} fail. Response: {r.status_code}, {r.text}")
        exit()

def _get_meeting_info(meeting_name, token, headers = {}):
    url = f"{base_address}:{admin_meeting_port}/meeting/meetingInfo"
    headers["Authorization"] = "Bearer " + token
    params = {
        "meetingName": meeting_name
    }
    r = requests.get(url, params=params, headers=headers)
    if r.status_code == 200:
        meeting_info = r.json()['responseBody']['meetingInfo']
        logging.info(f"get meeting info: {meeting_info}")
        return meeting_info
    else:
        logging.error(f"fail to get meeting info, {r.status_code}, {r.text}")
        exit()


if __name__ == '__main__':
    usernames = ["test222", "test333"]
    username = random.choice(usernames)
    token = _login(username, "a123456")

    user = _get_user_by_username(username, token)


    # random choose a meeting to submit articles
    # meetings = _get_available_meetings(username, token)
    # meeting = random.choice(meetings)
    # meeting_name = meeting['meetingName']

    meeting_name = "tdzNBhQQHj" # or just specify a meeting name here.

    meeting_info = _get_meeting_info(meeting_name, token)
    # logging.info(f"choose meeting {meeting_name}")

    # submit articles
    for i in range(6):
        _submit_an_article(user, token, meeting_info)

    chair_name = meeting_info["chairName"]
    chair_token = _login(chair_name)
    # begin the review
    # _begin_reivew(chair_name, chair_token, meeting_name)
    


    
