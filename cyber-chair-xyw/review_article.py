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

article_port = cp.get("server", "article_port")
meeting_port = cp.get("server", "meeting_port")
message_port = cp.get("server", "message_port")
pcmember_port = cp.get("server", "pcmember_port")
review_port = cp.get("server", "review_port")
user_port = cp.get("server", "user_port")

date = time.strftime("%Y-%m-%d", time.localtime())

def _get_pcmember_meetings(username):
    url = f"{base_address}:{pcmember_port}/user/pcMemberMeeting"
    params = {
        "username": username
    }
    r = requests.get(url, params=params)
    if r.status_code == 200:
        meetings = r.json()["responseBody"]["meetings"]
        logging.info(f"get {len(meetings)} {username}'s meetings as pc member.")
        return meetings
    else:
        logging.error(f"fail to get {username}'s meetings as pc member, {r.status_code}, {r.text}")

def _get_review_articles(username, meeting_name):
    url = f"{base_address}:{review_port}/meeting/reviewArticles"
    params = {
        "pcMemberName": username,
        "meetingName": meeting_name
    }
    r = requests.get(url, params=params)
    if r.status_code == 200:
        review_articles = r.json()["responseBody"]["reviewArticles"]
        logging.info(f"pc name: {username}, meeting name: {meeting_name}, get {len(review_articles)} review articles")
        return review_articles
    else:
        logging.error(f"{username} fail to get review articles, meeting: {meeting_name}, {r.status_code}, {r.text}")

def _review_article(username, articleId, score, confidence, reviews):
    url = f"{base_address}:{review_port}/meeting/reviewer"
    payload = {
        "pcMemberName": username,
        "articleid": articleId,
        "score": score,
        "confidence": confidence,
        "reviews": reviews
    }
    r = requests.post(url=url, json=payload)
    if r.status_code == 200:
        logging.info(f"{username} review {articleId} success. score: {score}, confidence: {confidence}, reviews: {reviews}, {r.text}")
    else:
        logging.error(f"{username} review {articleId} fail, {r.status_code}, {r.text}")

def _update_review(username, articleId, score, confidence, reviews, status):
    url = f"{base_address}:{review_port}/meeting/updateReview"
    payload = {
        "pcMemberName": username,
        "articleId": articleId,
        "score": score,
        "confidence": confidence,
        "reviews": reviews,
        "status": status
    }
    r = requests.post(url=url, json=payload)
    if r.status_code == 200:
        logging.info(f"{username} update review {articleId} success. score: {score}, confidence: {confidence}, reviews: {reviews}, {r.text}")
    else:
        logging.error(f"{username} review {articleId} fail, {r.status_code}, {r.text}")

def _confirm_review(username, articleId, status):
    url = f"{base_address}:{review_port}/meeting/reviewConfirm"
    payload = {
        "pcMemberName": username,
        "articleId": articleId,
        "status": status
    }
    r = requests.post(url=url, json=payload)
    if r.status_code == 200:
        logging.info(f"{username} confirm review {articleId} success. {r.text}")
    else:
        logging.error(f"{username} review {articleId} fail, {r.status_code}, {r.text}")

def _get_chair_meetings(username):
    url = f"{base_address}:{meeting_port}/user/chairMeeting"
    params = {"username": username}
    r = requests.get(url=url, params=params)
    if r.status_code == 200:
        meetings = r.json()["responseBody"]["meetings"]
        print(meetings)
        logging.info(f"{username} get {len(meetings)} chair meetings")
        return meetings
    else:
        logging.error(f"{username} get chair meetings failed, {r.status_code}, {r.text}")
    
    return None

def _publish_meeting(meeting_name):
    url = f"{base_address}:{meeting_port}/meeting/publish"
    payload = {
        "meetingName": meeting_name
    }
    r = requests.post(url, json=payload)
    if r.status_code == 200:
        logging.info(f"publish meeting {meeting_name} success, {r.text}")
    else:
        logging.error(f"publish meeting {meeting_name} fail, {r.status_code}, {r.text}")

if __name__ == '__main__':
    # review all articles
    users = _get_all_users()
    for user in users:
        username = user["username"]
        meetings = _get_pcmember_meetings(username)
        for meeting in meetings:
            meeting_name = meeting["meetingName"]
            review_articles = _get_review_articles(username, meeting_name)
            for article in review_articles:
                if article["reviewStatus"] == 'unReviewed':
                    _review_article(username, article["articleId"], -1, "high", "it's not good. I'd like to give a weak reject.")
    
    # chair end review and begin discussion
    chair_name = "wuxiya"
    chair_meetings = _get_chair_meetings(chair_name)
    for chair_meeting in chair_meetings:
        meeting_name = chair_meeting["meetingName"]
        meeting_info = _get_meeting_info(meeting_name)
        if meeting_info["status"] == 'ReviewCompleted':
            _publish_meeting(meeting_name)

    # re-review all articles
    for user in users:
        username = user["username"]
        meetings = _get_pcmember_meetings(username)
        for meeting in meetings:
            meeting_name = meeting["meetingName"]
            meeting_info = _get_meeting_info(meeting_name)
            if meeting_info["status"] == 'ResultPublished':
                review_articles = _get_review_articles(username, meeting_name)
                for article in review_articles:
                    if article["reviewStatus"] == 'alreadyReviewed':
                        _update_review(username, article["articleId"], 1, "high", "it's ok now.", "beforeRebuttal")
                        _confirm_review(username, article["articleId"], "beforeRebuttal")


        
        