import random
import time
import requests
import logging
from configparser import ConfigParser
from utils import random_str, random_form_list
from login import _login

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


def _create_conference(username, token, headers: dict = {}):
    logging.info(f"{username} apply a conference")
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
        "chairName": "test",
        "city": random_str(),
        "conferenceDate": date,
        "meetingName": random_str(),
        "notificationOfAcceptanceDate": date,
        "organizer": random_str(),
        "region": random.choice(regions),
        "submissionDeadlineDate": date,
        "topic": random_form_list(topics, random.randint(1, 5)),
        "venue": random_str(),
        "webPage": f"www.{random_str()}.com",
    }
    logging.debug(payload)

    r = requests.post(url=url, headers=headers, json=payload)

    if r.status_code == 200:
        logging.info(f"{username} apply conference {payload.get('meetingName')} success")
        data = {
            "meeting_name": payload.get("meetingName"),
            "topics": payload.get("topic"),
        }
        return data
    else:
        logging.error(f"{username} apply conference failed. payload: {payload}")

    return None


def _ratify(username, token, meeting_name, headers: dict = {}):
    logging.info(f"{username} start to ratify the meeting: {meeting_name}")
    url = f"{base_address}:{meeting_port}/admin/ratify"
    headers["Authorization"] = "Bearer " + token
    data = {
        "approvalStatus": "ApplyPassed",
        "meetingName": meeting_name,
    }

    r = requests.post(url=url, headers=headers, json=data)

    if r.status_code == 200:
        logging.info(f"Conference {meeting_name} ratify passed")
    else:
        logging.error(f"Conference {meeting_name} ratify failed with status_code: {r.status_code}, {r.text}")


def _get_all_users(without_chair = False, without_author = False):
    url = f"{base_address}:{user_port}/util/users?fullname="
    r = requests.get(url=url)

    if r.status_code == 200:
        logging.info("Get all users success")
        users: list = r.json().get("responseBody").get("users")

        # delete admin
        for user in users:
            if user["username"] == "admin":
                users.remove(user)
                break
        for user in users:
            if without_chair and user["username"] == "test":
                users.remove(user)
                break
        for user in users:
            if without_author and user["username"] == "akasaka":
                users.remove(user)
                break
        return users
    else:
        logging.error(f"Get all users failed, {r.status_code}, {r.text}")

    return None


def _invite_pcmember(chair_name, token, meeting_name, pc_name, headers: dict = {}):
    logging.info(f"{chair_name} start to invite {pc_name} for meeting {meeting_name}")
    url = f"{base_address}:{pcmember_port}/meeting/pcmInvitation"
    headers["Authorization"] = "Bearer " + token
    data = {
        "pcMemberName": pc_name,
        "meetingName": meeting_name,
    }
    r = requests.post(url=url, headers=headers, json=data)

    if r.status_code == 200:
        logging.info(f"Invite {pc_name} success")
    else:
        logging.error(f"Invite {pc_name} failed with status_code: {r.status_code}")


def _accept_invitation(pc_name, token, meeting_name, topics, headers: dict = {}):
    logging.info(f"{pc_name} start to accept the invitation of meeting {meeting_name}")
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
        logging.info(f"{pc_name} accept the invitation success")
    else:
        logging.error(f"{pc_name} accept the invitation failed, {r.status_code}, {r.text}")


def _begin_submission(chair_name, token, meeting_name, headers: dict = {}):
    logging.info(f"{chair_name} begin the submission of meeting {meeting_name}")

    url = f"{base_address}:{meeting_port}/meeting/beginSubmission"
    headers["Authorization"] = "Bearer " + token
    data = {
        "meetingName": meeting_name,
    }
    r = requests.post(url=url, headers=headers, json=data)
    if r.status_code == 200:
        logging.info(f"conference {meeting_name} begin submission success")
    else:
        logging.error(f"conference {meeting_name} begin submission failed, {r}")

def _begin_review(chair_name, token, meeting_name, headers: dict = {}, assignStrategy="TopicRelevant"):
    logging.info(f"{chair_name} begin the review of meeting {meeting_name}")

    url = f"{base_address}:{review_port}/meeting/beginReview"
    headers["Authorization"] = "Bearer " + token
    data = {
        "meetingName": meeting_name,
        "assignStrategy": assignStrategy
    }
    r = requests.post(url=url, headers=headers, json=data)
    if r.status_code == 200:
        logging.info(f"conference {meeting_name} begin reivew success")
    else:
        logging.error(f"conference {meeting_name} begin review failed, {r.status_code}, {r.text}")


if __name__ == '__main__':
    # admin login
    admin_token = _login("admin")
    chair_token = _login("test")

    # apply a meeting
    meeting = _create_conference("test", chair_token)
    meeting_name = meeting.get("meeting_name")
    
    topics = meeting.get("topics")

    # ratify the meeting
    _ratify("admin", admin_token, meeting_name)

    # invite three pc members
    users = _get_all_users(without_chair=True, without_author = True)
    pcmembers = random_form_list(users, 3)

    # accept the invitations
    for pc_member in pcmembers:
        pc_name = pc_member["username"]
        _invite_pcmember("test", chair_token, meeting_name, pc_name)
        pc_token = _login(pc_name, "123456")
        _accept_invitation(pc_name, pc_token, meeting_name, topics)

    # begin submission
    _begin_submission("test", chair_token, meeting_name)
