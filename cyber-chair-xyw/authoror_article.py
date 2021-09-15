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


def _get_author_meetings(username):

    url = f"{base_address}:{article_port}/user/authorMeeting"
    params = {
        "username": username
    }
    r = requests.get(url, params=params)
    if r.status_code == 200:
        meetings = r.json()["responseBody"]["meetings"]
        logging.info(f"get {len(meetings)} {username}'s meetings as author.")
        return meetings
    else:
        logging.error(f"fail to get {username}'s meetings as author, {r.status_code}, {r.text}")
    return []


def _get_author_submissions(author, meeting):
    url = f"{base_address}:{article_port}/meeting/submissionList"
    params = {
        "meetingName": meeting,
        "authorName": author
    }

    r = requests.get(url, params=params)
    if r.status_code == 200:
        logging.info(f"get author {author} submissions in meeting {meeting} success, {r.text}")
        subs = r.json()["responseBody"]["articles"]
        print(subs)
        return subs
    else:
        logging.error(f"get author {author} submissions in meeting {meeting} fail, {r.status_code}, {r.text}")
    return None


def _rebuttal(username, articleId, headers: dict = {}):
    url = f"{base_address}:{article_port}/meeting/rebuttal"
    token = _login(username)
    headers["Authorization"] = "Bearer " + token

    payload = {
        "articleId": articleId,
        "content": "I want to apply a rebuttal",
        "status": "rebuttal",
    }
    logging.debug(payload)

    r = requests.post(url=url, headers=headers, json=payload)

    if r.status_code == 200:
        logging.info(f"{username} apply rebuttal of article {payload.get('articleId')} success")
        res = r.json()
        return res
    else:
        logging.error(f"{username} apply rebuttal failed. payload: {payload}")

    return None


if __name__ == '__main__':
    # review all articles
    users = _get_all_users()
    for user in users:
        username = user["username"]
        meetings = _get_author_meetings(username)
        for meeting in meetings:
            meeting_name = meeting["meetingName"]
            meeting_info = _get_meeting_info(meeting_name)
            if meeting_info["status"] == 'ReviewConfirmed':
                submissions = _get_author_submissions(username, meeting_name)
                for article in submissions:
                    if article["status"] == "rejected":
                        # if article is rejected, commit a rebuttal
                        article_id = article["id"]
                        logging.info(f"{username} create a rebuttal for article {article_id} at meeting {meeting_name}")
                        _rebuttal(username, article_id)

