import random
from read_message import _get_notices
from submit_article import _get_available_meetings, _get_meeting_info
from rebuttal import _get_author_meetings, _get_author_submissions
from first_review_article import _get_chair_meetings, _get_pcmember_meetings, _get_review_articles
import requests
import logging
from configparser import ConfigParser
from login import _login

from create_and_start_conference import _get_all_users

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

def _get_article_detail(article_Id, token, headers = {}):
    url = f"{base_address}:{author_article_port}/user/articleDetail?articleId={article_Id}"
    headers["Authorization"] = "Bearer " + token

    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        logging.info(f"get article{article_Id} detail success.")
    else:
        logging.error(f"get article{article_Id} detail fail, {r.status_code}, {r.text}")

def _get_review(article_Id, token, headers = {}):
    url = f"{base_address}:{pcmember_port}/user/reviews?articleId={article_Id}"
    headers["Authorization"] = "Bearer " + token

    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        logging.info(f"get article{article_Id} review success.")
    else:
        logging.error(f"get article{article_Id} review fail, {r.status_code}, {r.text}")


if __name__ == '__main__':
    admin_token = _login("admin", "123456")

    users = _get_all_users("admin", admin_token)
    for user in users:
        username = user["username"]
        user_token = _login(username)
        meetings_chair = _get_chair_meetings(username, user_token)
        meetings_pc = _get_pcmember_meetings(username, user_token)
        meetings_author = _get_author_meetings(username, user_token)
        _get_available_meetings(username, user_token)
        _get_notices(username, user_token)

        if len(meetings_chair) != 0:
            meeting = random.choice(meetings_chair)
            meeting_name = meeting['meetingName']
            _get_meeting_info(meeting_name, user_token)

        if len(meetings_pc) != 0:
            meeting = random.choice(meetings_pc)
            meeting_name = meeting['meetingName']
            review_articles = _get_review_articles(username, user_token, meeting_name)
            article = random.choice(review_articles)
            article_id = article["articleId"]
            _get_article_detail(article_id, user_token)

        if len(meetings_author) != 0:
            meeting = random.choice(meetings_author)
            meeting_name = meeting['meetingName']
            submissions = _get_author_submissions(username, meeting_name, user_token)
            article = random.choice(submissions)
            _get_review(article_id, user_token)
