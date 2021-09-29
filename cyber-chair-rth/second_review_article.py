import random
import time
import requests
import logging
from configparser import ConfigParser
from utils import random_str, random_form_list
from login import _login

from create_and_start_conference import _get_all_users
from submit_article import _get_meeting_info

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

def _get_pcmember_meetings(username, token, headers = {}):
    url = f"{base_address}:{user_auth_port}/user/pcMemberMeeting"
    headers["Authorization"] = "Bearer " + token
    params = {
        "username": username
    }
    r = requests.get(url, params=params, headers=headers)
    if r.status_code == 200:
        meetings = r.json()["responseBody"]["meetings"]
        logging.info(f"get {len(meetings)} {username}'s meetings as pc member.")
        return meetings
    else:
        logging.error(f"fail to get {username}'s meetings as pc member, {r.status_code}, {r.text}")

def _get_review_articles(username, token, meeting_name, headers = {}):
    url = f"{base_address}:{pcmember_port}/meeting/reviewArticles"
    headers["Authorization"] = "Bearer " + token
    params = {
        "pcMemberName": username,
        "meetingName": meeting_name
    }
    r = requests.get(url, params=params, headers=headers)
    if r.status_code == 200:
        review_articles = r.json()["responseBody"]["reviewArticles"]
        logging.info(f"pc name: {username}, meeting name: {meeting_name}, get {len(review_articles)} review articles")
        return review_articles
    else:
        logging.error(f"{username} fail to get review articles, meeting: {meeting_name}, {r.status_code}, {r.text}")

def _update_review(username, token, articleId, score, confidence, reviews, status, headers = {}):
    url = f"{base_address}:{pcmember_port}/meeting/updateReview"
    headers["Authorization"] = "Bearer " + token
    payload = {
        "pcMemberName": username,
        "articleId": articleId,
        "score": score,
        "confidence": confidence,
        "reviews": reviews,
        "status": status
    }
    r = requests.post(url=url, json=payload, headers=headers)
    if r.status_code == 200:
        logging.info(f"{username} update review {articleId} success. score: {score}, confidence: {confidence}, reviews: {reviews}, {r.text}")
    else:
        logging.error(f"{username} review {articleId} fail, {r.status_code}, {r.text}")

def _confirm_review(username, token, articleId, status, headers = {}):
    url = f"{base_address}:{pcmember_port}/meeting/reviewConfirm"
    headers["Authorization"] = "Bearer " + token
    payload = {
        "pcMemberName": username,
        "articleId": articleId,
        "status": status
    }
    r = requests.post(url=url, json=payload, headers=headers)
    if r.status_code == 200:
        logging.info(f"{username} confirm review {articleId} success. {r.text}")
    else:
        logging.error(f"{username} review {articleId} fail, {r.status_code}, {r.text}")

def _get_chair_meetings(username, token, headers = {}):
    url = f"{base_address}:{user_auth_port}/user/chairMeeting"
    headers["Authorization"] = "Bearer " + token
    params = {"username": username}
    r = requests.get(url=url, params=params, headers=headers)
    if r.status_code == 200:
        meetings = r.json()["responseBody"]["meetings"]
        print(meetings)
        logging.info(f"{username} get {len(meetings)} chair meetings")
        return meetings
    else:
        logging.error(f"{username} get chair meetings failed, {r.status_code}, {r.text}")
    
    return None

def _final_publish_meeting(meeting_name, token, headers = {}):
    url = f"{base_address}:{chair_port}/meeting/finalPublish"
    headers["Authorization"] = "Bearer " + token
    payload = {
        "meetingName": meeting_name
    }
    r = requests.post(url, json=payload, headers=headers)
    if r.status_code == 200:
        logging.info(f"final publish meeting {meeting_name} success, {r.text}")
    else:
        logging.error(f"final publish meeting {meeting_name} fail, {r.status_code}, {r.text}")

if __name__ == '__main__':
    # admin login
    admin_token = _login("admin")

    # review all articles
    users = _get_all_users("admin", admin_token)
    for user in users:
        username = user["username"]
        pc_token = _login(username)
        meetings = _get_pcmember_meetings(username, pc_token)
        for meeting in meetings:
            meeting_name = meeting["meetingName"]
            review_articles = _get_review_articles(username, pc_token, meeting_name)
            for article in review_articles:
                if article["reviewStatus"] == 'reviewConfirmed':
                    _update_review(username, pc_token, article["articleId"], 2, "high", "it's ok now.", "afterRebuttal")
                    _confirm_review(username, pc_token, article["articleId"], "afterRebuttal")


    # chair end meeting
    chair_name = "test"
    chair_token = _login(chair_name)

    chair_meetings = _get_chair_meetings(chair_name, chair_token)
    for chair_meeting in chair_meetings:
        meeting_name = chair_meeting["meetingName"]
        meeting_info = _get_meeting_info(meeting_name, admin_token)
        if meeting_info["status"] == 'ReviewFinish':
            _final_publish_meeting(meeting_name, chair_token)