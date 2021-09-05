import random
import time
import requests
import logging
from configparser import ConfigParser
from utils import random_str, random_form_list

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


def _login(username="test123", password="12345qwert"):
    url = f"{base_address}:{user_auth_port}/login"
    headers = {
    }
    data = {
        "username": username,
        "password": password,
    }

    r = requests.post(url=url, headers=headers, json=data)

    if r.status_code == 200:
        data = r.json().get("responseBody")
        token = data.get("token")
        logging.info(f"Login success: {username}. token: {token}")
        return token
    else:
        logging.error(f"Login failed. status_code: {r.status_code}")
        exit()


if __name__ == '__main__':
    print(base_address)
    _login("admin", "Erangel")