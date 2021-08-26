import random
import time
import requests
from utils import random_str, random_form_list

base_address = "http://127.0.0.1"

article_port = "12803"
meeting_port = "12301"
message_port = "12406"
pcmember_port = "12305"
review_port = "12306"
user_port = "12401"

date = time.strftime("%Y-%m-%d", time.localtime())


def _login(username="wuxiya", password="123456"):
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


def _create_conference(token, headers: dict = {}):
    topics = ["Artificial intelligence",
              "Natural language processing",
              "Machine learning & data mining",
              "Computer vision",
              "The Web & information retrieval",
              "Computer architecture",
              "Computer networks",
              "Computer security",
              "Databases",
              "Design automation",
              "Embedded & real-time systems",
              "High-performance computing",
              "Mobile computing",
              "Measurement & perf. analysis",
              "Operating systems",
              "Programming languages",
              "Software engineering",
              "Algorithms & complexity",
              "Cryptography",
              "Logic & verification",
              "Comp. bio & bioinformatics",
              "Computer graphics",
              "Economics & computation",
              "Robotics",
              "Human-computer interaction",
              "Visualization"]

    regions = ["Austria",
               "China",
               "Egypt",
               "Greece",
               "Russia",
               "Romania",
               "Norway",
               "Japan"]

    url = f"{base_address}:{pcmember_port}/meeting/application"
    headers["Authorization"] = "Bearer " + token

    payload = {
        "acronym": random_str(),
        "chairName": "wuxiya",
        "city": random_str(),
        "conferenceDate": date,
        "meetingName": random_str(),
        "notificationOfAcceptanceDate": date,
        "organizer": random_str(),
        "region": random_form_list(regions),
        "submissionDeadlineDate": date,
        "topic": random_form_list(topics, random.randint(1, 5)),
        "venue": random_str(),
        "webPage": f"www.{random_str()}.com",
    }

    r = requests.post(url=url, headers=headers, json=payload)

    if r.status_code == 200:
        print(f"Apply conference {payload.get('meetingName')} success")
        data = {
            "meeting_name": payload.get("meetingName"),
            "topics": payload.get("topic"),
        }
        return data

    return None


def _ratify(token, meeting_name, headers: dict = {}):
    url = f"{base_address}:{meeting_port}/admin/ratify"
    headers["Authorization"] = "Bearer " + token
    data = {
        "approvalStatus": "ApplyPassed",
        "meetingName": meeting_name,
    }

    r = requests.post(url=url, headers=headers, json=data)

    if r.status_code == 200:
        print(f"Conference {meeting_name} ratify passed")
    else:
        print(f"Conference {meeting_name} ratify failed")


def _get_all_users(token, headers: dict = {}):
    url = f"{base_address}:{user_port}/util/users?fullname="
    headers["Authorization"] = "Bearer " + token
    r = requests.get(url=url, headers=headers)

    if r.status_code == 200:
        print(f"Get all users success")
        data = r.json().get("responseBody").get("users")
        users = []
        for i in data:
            users.append(i.get("username"))

        return users
    else:
        print(f"Get all users failed")

    return None


def _invite_pcmember(token, meeting_name, pc_name, headers: dict = {}):
    url = f"{base_address}:{pcmember_port}/meeting/pcmInvitation"
    headers["Authorization"] = "Bearer " + token
    data = {
        "pcMemberName": pc_name,
        "meetingName": meeting_name,
    }
    r = requests.post(url=url, headers=headers, json=data)

    if r.status_code == 200:
        print(f"Invite {pc_name} success")
    else:
        print(f"Invite {pc_name} failed")


def _accept_invitation(token, meeting_name, pc_name, topics, headers: dict = {}):
    url = f"{base_address}:{pcmember_port}/user/invitationRepo"
    headers["Authorization"] = "Bearer " + token
    data = {
        "username": pc_name,
        "meetingName": meeting_name,
        "response": "accepted",
        "topic": topics,
    }

    r = requests.post(url=url, headers=headers, json=data)
    if r.status_code == 200:
        print(f"{pc_name} accept Invitation success")
    else:
        print(f"{pc_name} accept Invitation failed")


def _begin_submission(token, meeting_name, headers: dict = {}):
    url = f"{base_address}:{meeting_port}/meeting/beginSubmission"
    headers["Authorization"] = "Bearer " + token
    data = {
        "meetingName": meeting_name,
    }
    r = requests.post(url=url, headers=headers, json=data)
    if r.status_code == 200:
        print(f"Conference {meeting_name} beginSubmission success")
    else:
        print(f"Conference {meeting_name} beginSubmission failed")


if __name__ == '__main__':
    admin_token = _login("admin")
    chair_token = _login()

    meeting = _create_conference(chair_token)
    meeting_name = meeting.get("meeting_name")
    topics = meeting.get("topics")


    _ratify(admin_token, meeting_name)
    _begin_submission(chair_token, meeting_name)

    users = _get_all_users(chair_token)
    pcmembers = random_form_list(users, 3)

    for i in pcmembers:
        _invite_pcmember(chair_token, meeting_name, i)
        pc_token = _login(i, "123456")
        _accept_invitation(pc_token, meeting_name, i, topics)
