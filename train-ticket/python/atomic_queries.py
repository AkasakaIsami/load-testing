from typing import List
import requests
from pprint import pprint
import logging
import time

logger = logging.getLogger("atomic_queries")
base_address = "http://10.176.122.1:31777"

headers = {
    "Cookie": "JSESSIONID=CAF07ABCB2031807D1C6043730C69F17; YsbCaptcha=ABF26F4AE563405894B1540057F62E7B",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmZHNlX21pY3Jvc2VydmljZSIsInJvbGVzIjpbIlJPTEVfVVNFUiJdLCJpZCI6IjRkMmE0NmM3LTcxY2ItNGNmMS1iNWJiLWI2ODQwNmQ5ZGE2ZiIsImlhdCI6MTYyNjM0NDgyNSwiZXhwIjoxNjI2MzQ4NDI1fQ.4eOMmQDhnq-Hjj1DuiH8duT6rXkP0QfeTnaXwvYGKD4",
    "Content-Type": "application/json"
}

# The UUID of fdse_microservice is that
uuid = "4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f"

date = time.strftime("%Y-%m-%d", time.localtime())



def _login(username="fdse_microservice", password="111111"):
    url = f"{base_address}/api/v1/users/login"

    cookies = {
        'JSESSIONID': '9ED5635A2A892A4BA31E7E98533A279D',
        'YsbCaptcha': '025080CF8BA94594B09E283F17815444',
    }

    headers = {
        'Proxy-Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Content-Type': 'application/json',
        'Origin': 'http://139.196.152.44:31000',
        'Referer': 'http://139.196.152.44:31000/client_login.html',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }

    data = '{"username":"' + username + '","password":"' + password + '","verificationCode":"1234"}'

    r = requests.post(url=url, headers=headers,
                      cookies=cookies, data=data, verify=False)

    if r.status_code == 200:
        print(r.text)
        data = r.json().get("data")
        uid = data.get("userId")
        token = data.get("token")

        return uid, token
    print(r.text)
    return None, None


def admin_login():
    pass


def _query_high_speed_ticket(place_pair: tuple = ("Shang Hai", "Su Zhou"), headers: dict = {}, time: str = "2021-07-15") -> List[str]:
    """
    返回TripId 列表
    :param place_pair: 使用的开始结束组对
    :param headers: 请求头
    :return: TripId 列表
    """

    url = f"{base_address}/api/v1/travelservice/trips/left"
    place_pairs = [("Shang Hai", "Su Zhou"),
                   ("Su Zhou", "Shang Hai"),
                   ("Nan Jing", "Shang Hai")]

    payload = {
        "departureTime": time,
        "startingPlace": place_pair[0],
        "endPlace": place_pair[1],
    }

    response = requests.post(url=url,
                             headers=headers,
                             json=payload)

    if response.status_code is not 200 or response.json().get("data") is None:
        logger.warning(f"request for {url} failed. response data is {response.text}")
        return None

    data = response.json().get("data")  # type: dict

    trip_ids = []
    for d in data:
        trip_id = d.get("tripId").get("type") + d.get("tripId").get("number")
        trip_ids.append(trip_id)
    return trip_ids


def _query_normal_ticket(place_pair: tuple = ("Nan Jing", "Shang Hai"), headers: dict = {}, time: str = "2021-07-15") -> List[str]:
    url = f"{base_address}/api/v1/travel2service/trips/left"
    place_pairs = [("Shang Hai", "Nan Jing"),
                   ("Nan Jing", "Shang Hai")]

    payload = {
        "departureTime": time,
        "startingPlace": place_pair[0],
        "endPlace": place_pair[1],
    }

    response = requests.post(url=url,
                             headers=headers,
                             json=payload)
    if response.status_code is not 200 or response.json().get("data") is None:
        logger.warning(f"request for {url} failed. response data is {response.json()}")
        return None

    data = response.json().get("data")  # type: dict

    trip_ids = []
    for d in data:
        trip_id = d.get("tripId").get("type") + d.get("tripId").get("number")
        trip_ids.append(trip_id)
    return trip_ids


def _query_advanced_ticket(place_pair: tuple = ("Nan Jing", "Shang Hai"), headers: dict = {}, time: str = "2021-07-15", type: str = "cheapest") -> List[str]:
    url = f"{base_address}/api/v1/travelplanservice/travelPlan/" + type
    print(url)
    
    payload = {
        "departureTime": time,
        "startingPlace": place_pair[0],
        "endPlace": place_pair[1],
    }

    #print(payload)

    response = requests.post(url=url,
                             headers=headers,
                             json=payload)
    #print(response.text)
    if response.status_code is not 200 or response.json().get("data") is None:
        logger.warning(f"request for {url} failed. response data is {response.json()}")
        return None
    
    data = response.json().get("data") 

    trip_ids = []
    for d in data:
        trip_id = d.get("tripId")
        trip_ids.append(trip_id)
    return trip_ids

def _query_assurances(headers: dict = {}):
    url = f"{base_address}/api/v1/assuranceservice/assurances/types"
    response = requests.get(url=url,headers=headers)
    if response.status_code is not 200 or response.json().get("data") is None:
        logger.warning(f"query assurance failed, response data is {response.json()}")
        return None
    data = response.json().get("data")
    # assurance只有一种

    return [{"assurance": "1"}]


def _query_food(place_pair: tuple = ("Shang Hai", "Su Zhou"), train_num: str = "D1345", headers: dict = {}):
    url = f"{base_address}/api/v1/foodservice/foods/2021-07-14/{place_pair[0]}/{place_pair[1]}/{train_num}"

    response = requests.get(url=url, headers=headers)
    if response.status_code is not 200 or response.json().get("data") is None:
        logger.warning(f"query food failed, response data is {response.json()}")
        return None
    data = response.json().get("data")

    # food 是什么不会对后续调用链有影响，因此查询后返回一个固定数值
    return [{
        "foodName": "Soup",
        "foodPrice": 3.7,
        "foodType": 2,
        "stationName": "Su Zhou",
        "storeName": "Roman Holiday"
    }]


def _query_contacts(headers: dict = {}) -> List[str]:
    """
    返回座位id列表
    :param headers:
    :return: id list
    """
    global uuid
    url = f"{base_address}/api/v1/contactservice/contacts/account/{uuid}"

    response = requests.get(url=url, headers=headers)
    if response.status_code is not 200 or response.json().get("data") is None:
        logger.warning(f"query contacts failed, response data is {response.json()}")
        return None

    data = response.json().get("data")
    #print("contacts")
    #pprint(data)


    ids = [d.get("id") for d in data if d.get("id") is not None]
    #pprint(ids)
    return ids


def _query_orders(headers: dict = {}, types: tuple = tuple([0]), query_other: bool = False) -> List[tuple]:
    """
    返回(orderId, tripId) triple list for inside_pay_service
    :param headers:
    :return:
    """
    url = ""

    if query_other:
        url = f"{base_address}/api/v1/orderOtherService/orderOther/refresh"
    else:
        url = f"{base_address}/api/v1/orderservice/order/refresh"

    payload = {
        "loginId": uuid,
    }

    response = requests.post(url=url, headers=headers, json=payload)
    if response.status_code is not 200 or response.json().get("data") is None:
        logger.warning(f"query orders failed, response data is {response.text}")
        return None

    data = response.json().get("data")
    pairs = []
    for d in data:
        # status = 0: not paid
        # status=1 paid not collect
        # status=2 collected
        if d.get("status") in types:
            order_id = d.get("id")
            trip_id = d.get("trainNumber")
            pairs.append((order_id, trip_id))
    print(f"queried {len(pairs)} orders")

    return pairs

def _query_orders_2(headers: dict = {}, types: tuple = tuple([0]), query_other: bool = False) -> List[tuple]:
    """
    返回(orderId, tripId) triple list for inside_pay_service
    :param headers:
    :return:
    """
    url = ""

    if query_other:
        url = f"{base_address}/api/v1/orderOtherService/orderOther/refresh"
    else:
        url = f"{base_address}/api/v1/orderservice/order/refresh"

    payload = {
        "loginId": uuid,
    }

    response = requests.post(url=url, headers=headers, json=payload)
    if response.status_code is not 200 or response.json().get("data") is None:
        logger.warning(f"query orders failed, response data is {response.text}")
        return None

    data = response.json().get("data")
    pairs = []
    for d in data:
        # status = 0: not paid
        # status=1 paid not collect
        # status=2 collected
        if d.get("status") in types:
            order_id = d.get("id")
            from_id = d.get("from")
            to_id = d.get("to")
            pairs.append((order_id, from_id, to_id))
    print(f"queried {len(pairs)} orders")

    return pairs
    

def _query_route(routeId: str = '92708982-77af-4318-be25-57ccb0ff69ad', headers: dict = {}):
    url = f"{base_address}/api/v1/routeservice/routes/{routeId}"

    res = requests.get(url=url, headers=headers)

    if res.status_code == 200:
        print(f"query {routeId} success")
    else:
        print(f"query {routeId} fail")

    return


def _pay_one_order(order_id, trip_id, headers: dict = {}):
    url = f"{base_address}/api/v1/inside_pay_service/inside_payment"
    payload = {
        "orderId": order_id,
        "tripId": trip_id
    }

    response = requests.post(url=url, headers=headers,
                             json=payload)

    if response.status_code == 200:
        print(f"{order_id} pay success")
    else:
        print(f"pay {order_id} failed!")
        return None

    return order_id


def _cancel_one_order(order_id, uuid, headers: dict = {}):
    url = f"{base_address}/api/v1/cancelservice/cancel/{order_id}/{uuid}"

    response = requests.get(url=url,
                            headers=headers)

    if response.status_code == 200:
        print(f"{order_id} cancel success")
    else:
        print(f"{order_id} cancel failed")

    return order_id


def _collect_one_order(order_id, headers: dict = {}):
    url = f"{base_address}/api/v1/executeservice/execute/collected/{order_id}"
    response = requests.get(url=url,
                            headers=headers)
    if response.status_code == 200:
        print(f"{order_id} collect success")
    else:
        print(f"{order_id} collect failed")

    return order_id


def _enter_station(order_id, headers: dict = {}):
    url = f"{base_address}/api/v1/executeservice/execute/execute/{order_id}"
    response = requests.get(url=url,
                            headers=headers)
    if response.status_code == 200:
        print(f"{order_id} enter station success")
    else:
        print(f"{order_id} enter station failed")

    return order_id


def _query_cheapest(date="2021-12-31", headers: dict = {}):
    url = f"{base_address}/api/v1/travelplanservice/travelPlan/cheapest"

    payload= {
        "departureTime": date,
        "endPlace": "Shang Hai",
        "startingPlace": "Nan Jing"
    }

    r = requests.post(url=url, json=payload, headers=headers)
    if r.status_code == 200:
        print("query cheapest success")
    else:
        print("query cheapest failed")


def _query_min_station(date="2021-12-31", headers: dict = {}):
    url = f"{base_address}/api/v1/travelplanservice/travelPlan/minStation"

    payload = {
        "departureTime": date,
        "endPlace": "Shang Hai",
        "startingPlace": "Nan Jing"
    }

    r = requests.post(url=url, json=payload, headers=headers)
    if r.status_code == 200:
        print("query min station success")
    else:
        print("query min station failed")


def _query_quickest(date="2021-12-31", headers: dict = {}):
    url = f"{base_address}/api/v1/travelplanservice/travelPlan/quickest"

    payload = {
        "departureTime": date,
        "endPlace": "Shang Hai",
        "startingPlace": "Nan Jing"
    }

    r = requests.post(url=url, json=payload, headers=headers)
    if r.status_code == 200:
        print("query quickest success")
    else:
        print("query quickest failed")


def _rebook_ticket(old_order_id, old_trip_id, new_trip_id, new_date, new_seat_type, headers):
    url = f"{base_address}/api/v1/rebookservice/rebook"

    payload = {
        "oldTripId": old_trip_id,
        "orderId": old_order_id,
        "tripId": new_trip_id,
        "date": new_date,
        "seatType": new_seat_type
    }
    print(payload)
    r = requests.post(url=url, json=payload, headers=headers)
    if r.status_code == 200:
        print(r.text)
    else:
        print(f"Request Failed: status code: {r.status_code}")
        print(r.text)

def _query_admin_travel(headers):
    url = f"{base_address}/api/v1/admintravelservice/admintravel"

    r = requests.get(url=url,headers=headers)
    if r.status_code == 200 and r.json()["status"] == 1:
        print("success to query admin travel")
    else:
        print(f"faild to query admin travel with status_code: {r.status_code}")



if __name__ == '__main__':
    #_query_food(headers=headers)
    #_query_high_speed_ticket(headers=headers)
    #_query_contacts(headers=headers)
    #_query_orders(headers=headers)
    #_pay_one_order("7502fb68-8433-44b6-b0a4-cc36651e0ea4",
    #               "Z1234",
    #               headers=headers)

    _, token = _login()

    headers = {
        "Cookie": "JSESSIONID=DBE6EC845809D4BFEA66D76BA600995F; YsbCaptcha=63EEEE0E2D564384A7C0052999F3AEA6",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmZHNlX21pY3Jvc2VydmljZSIsInJvbGVzIjpbIlJPTEVfVVNFUiJdLCJpZCI6IjRkMmE0NmM3LTcxY2ItNGNmMS1iNWJiLWI2ODQwNmQ5ZGE2ZiIsImlhdCI6MTYyNjM0OTcxOSwiZXhwIjoxNjI2MzUzMzE5fQ.nUTB1SI_gikEm8z8M6EQeyPuQx5zKevo40Y2rqf1EN4",
        "Content-Type": "application/json"
    }
    headers["Authorization"] = "Bearer " + token

    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    for i in range(300):
        _query_admin_travel(headers=headers)
        print("*****************************INDEX:" + str(i))
    
    end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"start:{start_time} end:{end_time}")
