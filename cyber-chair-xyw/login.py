
import time
import requests

base_address = "http://127.0.0.1"

article_port = "12803"
meeting_port = "12301"
message_port = "12406"
pcmember_port = "12305"
review_port = "12306"
user_port = "12401"

date = time.strftime("%Y-%m-%d", time.localtime())

def _login(username="wuxiya", password="Pwuxiya"):
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
        print("login success")
        return token

    print(r.text)
    return None
