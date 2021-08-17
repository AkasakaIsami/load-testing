import requests
import time

from atomic_queries import _login, _query_orders_2, _pay_one_order
from utils import random_form_list

base_address = "http://10.176.122.1:31777"
uuid = "4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f"
date1 = time.strftime("%Y-%m-%d", time.localtime())
date2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def query_and_update_consign(headers):
    """
    查询Order并更新托运信息
    :return:
    """
    pairs = _query_orders_2(headers=headers, types=tuple([0, 1, 3]))
    pairs2 = _query_orders_2(
        headers=headers, types=tuple([0, 1, 3]), query_other=True)

    if not pairs and not pairs2:
        return

    pairs = pairs + pairs2

    # (orderId, tripId) pair
    pair = random_form_list(pairs)

    url = f"{base_address}/api/v1/consignservice/consigns/order/{pair[0]}"

    response = requests.get(url=url, headers=headers)
    if response.status_code is not 200 or response.json().get("data") is None:
        return None

    data = response.json().get("data")
    consign = data.get("id")

    url = f"{base_address}/api/v1/consignservice/consigns"

    payload = {
        "accountId": uuid,
        "consignee": "test consignee",
        "from": pair[1],
        "handleDate": date1,
        "id": consign,
        "isWithin": False,
        "orderId": pair[0],
        "phone": "11111111111",
        "targetDate": date2,
        "to": pair[2],
        "weight": "100",
    }

    requests.put(url=url,
                 headers=headers,
                 json=payload)



if __name__ == '__main__':
    _, token = _login()

    headers = {
        "Cookie": "JSESSIONID=CAF07ABCB2031807D1C6043730C69F17; YsbCaptcha=ABF26F4AE563405894B1540057F62E7B",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmZHNlX21pY3Jvc2VydmljZSIsInJvbGVzIjpbIlJPTEVfVVNFUiJdLCJpZCI6IjRkMmE0NmM3LTcxY2ItNGNmMS1iNWJiLWI2ODQwNmQ5ZGE2ZiIsImlhdCI6MTYyNjM0NDgyNSwiZXhwIjoxNjI2MzQ4NDI1fQ.4eOMmQDhnq-Hjj1DuiH8duT6rXkP0QfeTnaXwvYGKD4",
        "Content-Type": "application/json"
    }
    headers["Authorization"] = "Bearer " + token

    for i in range(3):
        query_and_update_consign(headers=headers)
