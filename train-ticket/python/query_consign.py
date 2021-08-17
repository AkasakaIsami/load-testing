from atomic_queries import _login
import requests

base_address = "http://139.196.152.44:31000"
uuid = "4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f"

def query_consign(headers):
    """
    查询所有托运信息
    :return:
    """

    url = f"{base_address}/api/v1/consignservice/consigns/account/{uuid}"

    response = requests.get(url=url, headers=headers)
    if response.status_code is not 200 or response.json().get("data") is None:
        return None


if __name__ == '__main__':
    _, token = _login()

    headers = {
        "Cookie": "JSESSIONID=CAF07ABCB2031807D1C6043730C69F17; YsbCaptcha=ABF26F4AE563405894B1540057F62E7B",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmZHNlX21pY3Jvc2VydmljZSIsInJvbGVzIjpbIlJPTEVfVVNFUiJdLCJpZCI6IjRkMmE0NmM3LTcxY2ItNGNmMS1iNWJiLWI2ODQwNmQ5ZGE2ZiIsImlhdCI6MTYyNjM0NDgyNSwiZXhwIjoxNjI2MzQ4NDI1fQ.4eOMmQDhnq-Hjj1DuiH8duT6rXkP0QfeTnaXwvYGKD4",
        "Content-Type": "application/json"
    }
    headers["Authorization"] = "Bearer " + token

    query_consign(headers=headers)
