import random
import time
from login import _login
from utils import random_form_list

base_address = "http://127.0.0.1"

article_port = "12803"
meeting_port = "12301"
message_port = "12406"
pcmember_port = "12305"
review_port = "12306"
user_port = "12401"

date = time.strftime("%Y-%m-%d", time.localtime())

if __name__ == '__main__':
    submitters = ["test2", "test3"]
    submitter_token = _login(random.choice(submitters), "123456")
