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


def _get_notices(username, token, headers={}):
    url = f"{base_address}:{notice_port}/notice?receiver={username}&state=0"
    headers["Authorization"] = "Bearer " + token
    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        notices_json = r.json()
        if "responseBody" in notices_json:
            notices = notices_json["responseBody"]
            logging.info(f"get {len(notices)} {username}'s unread notices.")
            return notices
        else: 
            logging.info(f"get 0 {username}'s unread notices.")
            return []   
    else:
        logging.error(
            f"fail to get {username}'s unread notices, {r.status_code}, {r.text}")


def _read_notice(username, token, notice_id, headers={}):
    url = f"{base_address}:{notice_port}/notice"
    headers["Authorization"] = "Bearer " + token

    payload = {
        "id": notice_id
    }

    r = requests.put(url, json=payload, headers=headers)

    if r.status_code == 200:
        logging.info(f"user {username} read notice{notice_id} success.")
    else:
        logging.error(
            f"user {username} read notice{notice_id} fail, {r.status_code}, {r.text}")


if __name__ == '__main__':
    # admin login
    admin_token = _login("admin", "123456")

    # review all articles
    users = _get_all_users("admin", admin_token)
    for user in users:
        username = user["username"]
        user_token = _login(username)
        notices = _get_notices(username, user_token)

        for notice in notices:
            notice_id = notice["id"]
            _read_notice(username, user_token, notice_id)