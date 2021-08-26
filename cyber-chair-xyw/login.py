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

article_port = cp.get("server", "article_port")
meeting_port = cp.get("server", "meeting_port")
message_port = cp.get("server", "message_port")
pcmember_port = cp.get("server", "pcmember_port")
review_port = cp.get("server", "review_port")
user_port = cp.get("server", "user_port")

date = time.strftime("%Y-%m-%d", time.localtime())


def _login(username="wuxiya", password="123456"):
    logging.info(f"Log in with user: {username}")

    url = f"{base_address}:{user_port}/login"
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
        logging.info(f"Login success: {username}")
        return token
    else:
        logging.error(f"login failed. status_code: {r.status_code}")

    return None

if __name__ == '__main__':
    print(base_address)