import time
import requests
import logging
from configparser import ConfigParser
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


def _get_author_meetings(username, token, headers = {}):
    headers["Authorization"] = "Bearer " + token

    url = f"{base_address}:{user_auth_port}/user/authorMeeting"
    params = {
        "username": username
    }
    r = requests.get(url, params=params, headers=headers)

    if r.status_code == 200:
        meetings = r.json()["responseBody"]["meetings"]
        logging.info(f"get {len(meetings)} {username}'s meetings as author.")
        return meetings
    else:
        logging.error(f"fail to get {username}'s meetings as author, {r.status_code}, {r.text}")
    return []

def _get_author_submissions(author, meeting, token, headers = {}):
    headers["Authorization"] = "Bearer " + token

    url = f"{base_address}:{author_article_port}/meeting/submissionList"
    params = {
        "meetingName": meeting,
        "authorName": author
    }

    r = requests.get(url, params=params,  headers=headers)
    if r.status_code == 200:
        logging.info(f"get author {author} submissions in meeting {meeting} success, {r.text}")
        subs = r.json()["responseBody"]["articles"]
        print(subs)
        return subs
    else:
        logging.error(f"get author {author} submissions in meeting {meeting} fail, {r.status_code}, {r.text}")
    return None

def _rebuttal(username, articleId, token, headers: dict = {}):
    url = f"{base_address}:{pcmember_port}/meeting/rebuttal"
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
    author_token = _login("akasaka")

    username = "akasaka"
    meetings = _get_author_meetings(username, author_token)
    for meeting in meetings:
        meeting_name = meeting["meetingName"]
        meeting_info = _get_meeting_info(meeting_name, token=author_token)
        if meeting_info["status"] == 'ReviewConfirmed':
            submissions = _get_author_submissions(username, meeting_name, token=author_token)

            for article in submissions:
                if article["status"] == "rejected" or article["status"] == "accepted":
                    # if article is rejected, commit a rebuttal
                    article_id = article["id"]
                    logging.info(f"{username} create a rebuttal for article {article_id} at meeting {meeting_name}")
                    _rebuttal(username, article_id, token=author_token)