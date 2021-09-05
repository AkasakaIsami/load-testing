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

def _register(username, password, fullname):
    url = f"{base_address}:{user_auth_port}/register"
    payload = {
        "username": username,
        "password": password,
        "fullname": fullname,
        "email": username + "@fudan.edu.cn",
        "region": "China",
        "institution": "Fudan",
        "authorities": [""]
    }
    r = requests.post(url=url, json=payload)
    logging.info(f"register user {username}, {r.status_code}, {r.text}")


if __name__ == '__main__':
    _register("test111", "a123456", "test one")
    _register("test222", "a123456", "test two")
    _register("test333", "a123456", "test three")
    _register("test444", "a123456", "test four")
    _register("test999", "a123456", "test nine")