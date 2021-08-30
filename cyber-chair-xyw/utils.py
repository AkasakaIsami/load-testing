import random
from typing import List
import string


def random_boolean() -> bool:
    return random.choice([True, False])


def random_form_list(l: List, num=1):
    # if num == 1:
    #     return random.choice(l)
    return random.sample(l,num)



def random_str():
    return ''.join(random.choices(string.ascii_letters, k=random.randint(4, 10)))


def random_phone():
    return ''.join(random.choices(string.digits, k=random.randint(8, 15)))
