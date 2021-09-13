from configparser import ConfigParser
import logging
import time
import requests
from atomic_queries import _login
from utils import random_phone, random_uuid, random_str, random_form_list, random_rate

cp = ConfigParser()
cp.read("config.ini")

logger = logging.getLogger("admin_operations")
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

base_address = cp.get("server", "base_address")
user_uuid = cp.get("server", "uuid")
time_now = int(round(time.time() * 1000))


def _get_orders(headers={}):
    url = f"{base_address}/api/v1/adminorderservice/adminorder"

    r = requests.get(url=url, headers=headers)

    if r.status_code == 200:
        orders = r.json()["data"]
        logging.info(f"Get {len(orders)} orders")
        return orders
    else:
        logging.error(r)


def _get_routes(headers={}):
    url = f"{base_address}/api/v1/adminrouteservice/adminroute"

    r = requests.get(url=url, headers=headers)

    if r.status_code == 200:
        routes = r.json()["data"]
        logging.info(f"Get {len(routes)} routes")
        return routes
    else:
        logging.error(r)


def _get_travels(headers={}):
    url = f"{base_address}/api/v1/admintravelservice/admintravel"

    r = requests.get(url=url, headers=headers)

    if r.status_code == 200:
        travels = r.json()["data"]
        logging.info(f"Get {len(travels)} travels")
        return travels
    else:
        logging.error(r)


def _get_users(headers={}):
    url = f"{base_address}/api/v1/adminuserservice/users"

    r = requests.get(url=url, headers=headers)

    if r.status_code == 200:
        users = r.json()["data"]
        logging.info(f"Get {len(users)} users")
        return users
    else:
        logging.error(r)


def _get_contacts(headers={}):
    url = f"{base_address}/api/v1/adminbasicservice/adminbasic/contacts"

    r = requests.get(url=url, headers=headers)

    if r.status_code == 200:
        contacts = r.json()["data"]
        logging.info(f"Get {len(contacts)} contacts")
        return contacts
    else:
        logging.error(r)


def _get_stations(headers={}):
    url = f"{base_address}/api/v1/adminbasicservice/adminbasic/stations"

    r = requests.get(url=url, headers=headers)

    if r.status_code == 200:
        stations = r.json()["data"]
        logging.info(f"Get {len(stations)} stations")
        return stations
    else:
        logging.error(r)


def _get_trains(headers={}):
    url = f"{base_address}/api/v1/adminbasicservice/adminbasic/trains"

    r = requests.get(url=url, headers=headers)

    if r.status_code == 200:
        trains = r.json()["data"]
        logging.info(f"Get {len(trains)} trains")
        return trains
    else:
        logging.error(r)


def _get_prices(headers={}):
    url = f"{base_address}/api/v1/adminbasicservice/adminbasic/prices"

    r = requests.get(url=url, headers=headers)

    if r.status_code == 200:
        prices = r.json()["data"]
        logging.info(f"Get {len(prices)} prices")
        return prices
    else:
        logging.error(r)


def _get_configs(headers={}):
    url = f"{base_address}/api/v1/adminbasicservice/adminbasic/configs"

    r = requests.get(url=url, headers=headers)

    if r.status_code == 200:
        configs = r.json()["data"]
        logging.info(f"Get {len(configs)} configs")
        return configs
    else:
        logging.error(r)


def _add_order(headers={}):
    url = f"{base_address}/api/v1/adminorderservice/adminorder"

    seat_num = random_phone()

    payload = {
        "accountId": "4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f",
        "boughtDate": time_now,
        "coachNumber": 5,
        "contactsDocumentNumber": "DocumentNumber_One",
        "contactsName": "Contacts_One",
        "documentType": 1,
        "from": "shanghai",
        "price": "22.5",
        "seatClass": 3,
        "seatNumber": seat_num,
        "status": 0,
        "to": "suzhou",
        "trainNumber": "D1345",
        "travelDate": time_now,
        "travelTime": time_now
    }
    r = requests.post(url=url, json=payload, headers=headers)

    if r.status_code == 200:
        order_id = r.json()["data"]["id"]
        order = r.json()["data"]
        print(order["accountId"])
        logging.info(f"Create order {order_id} success")
        return order
    else:
        logging.error(r)


def _update_order(order_id, headers={}):
    url = f"{base_address}/api/v1/adminorderservice/adminorder"

    new_seat_num = random_phone()

    payload = {
        "id": order_id,
        "accountId": "4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f",
        "boughtDate": time_now,
        "coachNumber": 5,
        "contactsDocumentNumber": "DocumentNumber_One",
        "contactsName": "Contacts_One",
        "documentType": 1,
        "from": "shanghai",
        "price": "22.5",
        "seatClass": 3,
        "seatNumber": new_seat_num,
        "status": 0,
        "to": "suzhou",
        "trainNumber": "D1345",
        "travelDate": time_now,
        "travelTime": time_now
    }
    r = requests.put(url=url, json=payload, headers=headers)

    if r.status_code == 200:
        logging.info(
            f"Modify order {order_id} success, seatNumber change to {new_seat_num}")
    else:
        logging.error(r)


def _delete_order(order_id, order_train_num, headers={}):
    url = f"{base_address}/api/v1/adminorderservice/adminorder/{order_id}/{order_train_num}"

    r = requests.delete(url=url, headers=headers)

    if r.status_code == 200:
        logging.info(
            f"Delete order {order_id} success")
    else:
        logging.error(r)


def _add_route(headers={}):
    url = f"{base_address}/api/v1/adminrouteservice/adminroute"

    payload = {
        "distanceList": "0,100",
        "endStation": "nanjing",
        "startStation": "suzhou",
        "stationList": "suzhou,nanjing"
    }

    r = requests.post(url=url, json=payload, headers=headers)

    if r.status_code == 200:
        logging.info(f"Create Route [suzhou,nanjing] success")
    else:
        logging.error(r)


def _update_route(headers={}):
    routes = _get_routes(headers=headers)
    route_id = ""
    for route in routes:
        if route["stations"] == ["suzhou", "nanjing"]:
            route_id = route["id"]

    url = f"{base_address}/api/v1/adminrouteservice/adminroute"
    payload = {
        "distanceList": "0,120",
        "endStation": "nanjing",
        "startStation": "suzhou",
        "stationList": "suzhou,nanjing",
        "id": route_id
    }

    r = requests.put(url=url, json=payload, headers=headers)

    if r.status_code == 200:
        logging.info(
            f"Update Route [suzhou,nanjing] success, change distanceList from 0,100 to 0,120")
        return route_id
    else:
        logging.error(r)


def _delete_route(route_id, headers={}):
    url = f"{base_address}/api/v1/adminrouteservice/adminroute/{route_id}"

    r = requests.delete(url=url, headers=headers)

    if r.status_code == 200:
        logging.info(
            f"Delete Route [suzhou,nanjing] success")
    else:
        logging.error(r)


def _add_user(headers={}):
    url = f"{base_address}/api/v1/adminuserservice/users"
    username = random_str()
    payload = {
        "documentNum": random_phone(),
        "documentType": 1,
        "email": random_str()+"@"+random_str()+"."+random_str(),
        "gender": random_form_list([1, 2]),
        "password": random_phone(),
        "userName": username,
    }
    r = requests.post(url=url, json=payload, headers=headers)

    if r.status_code == 200:
        logging.info(f"Create user {username} success")
        return username
    else:
        logging.error(r)


def _update_user(username, headers={}):
    users = _get_users(headers=headers)
    user_id = ""
    for user in users:
        if user["userName"] == username:
            user_id = user["userId"]

    url = f"{base_address}/api/v1/adminuserservice/users"
    payload = {
        "accountId": user_id,
        "documentNum": random_phone(),
        "documentType": 1,
        "email": random_str()+"@"+random_str()+"."+random_str(),
        "gender": random_form_list([1, 2]),
        "password": random_phone(),
        "userName": username,
    }
    r = requests.put(url=url, json=payload, headers=headers)

    if r.status_code == 200:
        logging.info(f"Update user {username} success")
        return username
    else:
        logging.error(r)


def _delete_user(username, headers={}):
    users = _get_users(headers=headers)
    user_id = ""
    for user in users:
        if user["userName"] == username:
            user_id = user["userId"]

    url = f"{base_address}/api/v1/adminuserservice/users/{user_id}"

    r = requests.delete(url=url, headers=headers)

    if r.status_code == 200:
        logging.info(
            f"Delete user {username} success")
    else:
        logging.error(r)


def _add_contact(headers={}):
    url = f"{base_address}/api/v1/adminbasicservice/adminbasic/contacts"

    name = random_str()
    payload = {
        "accountId": user_uuid,
        "documentNumber": random_phone(),
        "documentType": random_form_list([1, 2]),
        "name": name,
        "phoneNumber": random_phone()
    }

    r = requests.post(url=url, json=payload, headers=headers)

    if r.status_code == 200:
        logging.info(f"Create contact {name} success")
        return name
    else:
        logging.error(r)


def _update_contact(name, headers={}):
    contacts = _get_contacts(headers=headers)
    contact_id = ""
    for contact in contacts:
        if contact["name"] == name:
            contact_id = contact["id"]

    url = f"{base_address}/api/v1/adminbasicservice/adminbasic/contacts"
    payload = {
        "id": contact_id,
        "documentNumber": random_phone(),
        "documentType": random_form_list([1, 2]),
        "name": name,
        "phoneNumber": random_phone()
    }

    r = requests.put(url=url, json=payload, headers=headers)

    if r.status_code == 200:
        logging.info(f"Update contact {name} success")
        return name
    else:
        logging.error(r)


def _delete_contact(name, headers={}):
    contacts = _get_contacts(headers=headers)
    contact_id = ""
    for contact in contacts:
        if contact["name"] == name:
            contact_id = contact["id"]

    url = f"{base_address}/api/v1/adminbasicservice/adminbasic/contacts/{contact_id}"

    r = requests.delete(url=url, headers=headers)

    if r.status_code == 200:
        logging.info(
            f"Delete contact {name} success")
    else:
        logging.error(r)


def _add_station(headers={}):
    url = f"{base_address}/api/v1/adminbasicservice/adminbasic/stations"

    payload = {
        "id": "chongqing",
        "name": "Chong Qing",
        "stayTime": 5,
    }

    r = requests.post(url=url, json=payload, headers=headers)

    if r.status_code == 200:
        logging.info(f"Create Station Chong Qing success")
    else:
        logging.error(r)


def _update_station(headers={}):
    url = f"{base_address}/api/v1/adminbasicservice/adminbasic/stations"
    payload = {
        "id": "chongqing",
        "name": "Chong Qing",
        "stayTime": 10
    }

    r = requests.put(url=url, json=payload, headers=headers)

    if r.status_code == 200:
        logging.info(
            f"Update station Chong Qing success, change stay time from 5 to 10")
    else:
        logging.error(r)


def _delete_station(headers={}):
    url = f"{base_address}/api/v1/adminbasicservice/adminbasic/stations"

    payload = {
        "id": "chongqing",
        "name": "Chong Qing",
        "stayTime": 10
    }

    r = requests.delete(url=url, json=payload, headers=headers)

    if r.status_code == 200:
        logging.info(
            f"Delete station Chong Qing success")
    else:
        logging.error(r)


def _add_train(headers={}):
    url = f"{base_address}/api/v1/adminbasicservice/adminbasic/trains"

    new_id = random_str()
    payload = {
        "averageSpeed": 100,
        "confortClass": 9999999,
        "economyClass": 9999999,
        "id": new_id
    }

    r = requests.post(url=url, json=payload, headers=headers)

    if r.status_code == 200:
        logging.info(f"Create train {new_id} success")
        return new_id
    else:
        logging.error(r)


def _update_train(id, headers={}):
    url = f"{base_address}/api/v1/adminbasicservice/adminbasic/trains"
    payload = {
        "averageSpeed": 120,
        "confortClass": 9999999,
        "economyClass": 9999999,
        "id": id
    }

    r = requests.put(url=url, json=payload, headers=headers)

    if r.status_code == 200:
        logging.info(
            f"Update train {id} success, change averageSpeed from 100 to 120")
    else:
        logging.error(r)


def _delete_train(id, headers={}):
    url = f"{base_address}/api/v1/adminbasicservice/adminbasic/trains/{id}"

    r = requests.delete(url=url, headers=headers)

    if r.status_code == 200:
        logging.info(
            f"Delete train {id} success")
    else:
        logging.error(r)


def _add_price(headers={}):
    route_id = random_str()
    train_id = random_str()

    url = f"{base_address}/api/v1/adminbasicservice/adminbasic/prices"

    payload = {
        "basicPriceRate": random_rate(),
        "firstClassPriceRate": 1,
        "routeId": route_id,
        "trainType": train_id
    }

    r = requests.post(url=url, json=payload, headers=headers)

    if r.status_code == 200:
        prices = _get_prices(headers=headers)
        price_id = ""
        for price in prices:
            if price["routeId"] == route_id and price["trainType"] == train_id:
                price_id = price["id"]
                break

        logging.info(f"Create price {price_id} success")

        return price_id
    else:
        logging.error(r)


def _update_price(price_id, headers={}):

    url = f"{base_address}/api/v1/adminbasicservice/adminbasic/prices"
    payload = {
        "basicPriceRate": random_rate(),
        "firstClassPriceRate": 1,
        "id": price_id,
        "routeId": random_str(),
        "trainType": random_str()
    }

    r = requests.put(url=url, json=payload, headers=headers)

    if r.status_code == 200:
        logging.info(
            f"Update Price {price_id} success")
    else:
        logging.error(r)

# FIXME: frontend fail to send the request body


def _delete_price(price_id, headers={}):
    prices = _get_prices(headers=headers)
    payload = {}

    for price in prices:
        if price["id"] == price_id:
            payload = {
                "basicPriceRate": price["basicPriceRate"],
                "firstClassPriceRate": price["firstClassPriceRate"],
                "id": price_id,
                "routeId": price["routeId"],
                "trainType": price["trainType"]
            }
            break

    url = f"{base_address}/api/v1/adminbasicservice/adminbasic/prices"

    r = requests.delete(url=url, json=payload, headers=headers)

    if r.status_code == 200:
        logging.info(
            f"Delete Price {price_id} success")
    else:
        logging.error(r)


def _add_config(headers={}):
    url = f"{base_address}/api/v1/adminbasicservice/adminbasic/configs"

    new_name = random_str()
    payload = {
        "description": random_str(),
        "name": new_name,
        "value": random_rate()
    }

    r = requests.post(url=url, json=payload, headers=headers)

    if r.status_code == 200:
        logging.info(f"Create config {new_name} success")
        return new_name
    else:
        logging.error(r)


def _update_config(name, headers={}):
    url = f"{base_address}/api/v1/adminbasicservice/adminbasic/configs"
    payload = {
        "description": random_str(),
        "name": name,
        "value": random_rate()
    }

    r = requests.put(url=url, json=payload, headers=headers)

    if r.status_code == 200:
        logging.info(
            f"Update config {name} success")
    else:
        logging.error(r)


def _delete_config(name, headers={}):
    url = f"{base_address}/api/v1/adminbasicservice/adminbasic/configs/{name}"

    r = requests.delete(url=url, headers=headers)

    if r.status_code == 200:
        logging.info(
            f"Delete config {name} success")
    else:
        logging.error(r)

# FIXME: frontend missing some data: endTime, startingStationId, and terminalStationId


def _add_travel(headers={}):
    route_id = random_form_list(_get_routes(headers=headers))["id"]

    url = f"{base_address}/api/v1/admintravelservice/admintravel"

    payload = {
        "routeId": route_id,
        "startingTime": time_now,
        "trainTypeId": "ZhiDa",
        "tripId": "Z233",
        "endTime": time_now,
        "startingStationId": "shanghai",
        "terminalStationId": "nanjing"
    }

    r = requests.post(url=url, json=payload, headers=headers)

    if r.status_code == 200:
        logging.info(f"Create Travel Z233 success")
    else:
        logging.error(r)


# FIXME: frontend missing some data: endTime, startingStationId, and terminalStationId

def _update_travel(headers={}):
    route_id = random_form_list(_get_routes(headers=headers))["id"]

    url = f"{base_address}/api/v1/admintravelservice/admintravel"
    payload = {
        "routeId": route_id,
        "startingTime": time_now,
        "trainTypeId": "ZhiDa",
        "tripId": "Z233",
        "endTime": time_now,
        "startingStationId": "shanghai",
        "terminalStationId": "beijing"
    }

    r = requests.put(url=url, json=payload, headers=headers)

    if r.status_code == 200:
        logging.info(
            f"Update Travel Z233 success")
    else:
        logging.error(r)


def _delete_travel(headers={}):
    url = f"{base_address}/api/v1/admintravelservice/admintravel/Z233"

    r = requests.delete(url=url, headers=headers)

    if r.status_code == 200:
        logging.info(
            f"Delete Travel Z233 success")
    else:
        logging.error(r)


def _get(headers={}):
    _get_orders(headers=headers)
    _get_routes(headers=headers)
    _get_travels(headers=headers)
    _get_users(headers=headers)
    _get_contacts(headers=headers)
    _get_stations(headers=headers)
    _get_trains(headers=headers)
    _get_prices(headers=headers)
    _get_configs(headers=headers)


def _add_update_delete(headers={}):
    order = _add_order(headers=headers)
    order_id = order["id"]
    order_train_num = order["trainNumber"]
    _update_order(order_id=order_id, headers=headers)
    _delete_order(order_id=order_id,
                  order_train_num=order_train_num, headers=headers)

    _add_route(headers=headers)
    route_id = _update_route(headers=headers)
    _delete_route(route_id=route_id, headers=headers)

    _add_travel(headers=headers)
    _update_travel(headers=headers)
    _delete_travel(headers=headers)

    username = _add_user(headers=headers)
    _update_user(username=username, headers=headers)
    _delete_user(username=username, headers=headers)

    name = _add_contact(headers=headers)
    _update_contact(name=name, headers=headers)
    _delete_contact(name=name, headers=headers)

    _add_station(headers=headers)
    _update_station(headers=headers)
    _delete_station(headers=headers)

    train_id = _add_train(headers=headers)
    _update_train(id=train_id, headers=headers)
    _delete_train(id=train_id, headers=headers)

    price_id = _add_price(headers=headers)
    _update_price(price_id=price_id, headers=headers)
    _delete_price(price_id=price_id, headers=headers)

    config_name = _add_config(headers=headers)
    _update_config(name=config_name, headers=headers)
    _delete_config(name=config_name, headers=headers)


if __name__ == '__main__':
    _, token = _login("admin", "222222")
    headers = {
        "Cookie": "JSESSIONID=823B2652E3F5B64A1C94C924A05D80AF; YsbCaptcha=2E037F4AB09D49FA9EE3BE4E737EAFD2",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmZHNlX21pY3Jvc2VydmljZSIsInJvbGVzIjpbIlJPTEVfVVNFUiJdLCJpZCI6IjRkMmE0NmM3LTcxY2ItNGNmMS1iNWJiLWI2ODQwNmQ5ZGE2ZiIsImlhdCI6MTYyNzE5OTA0NCwiZXhwIjoxNjI3MjAyNjQ0fQ.3IIwwz7AwqHtOFDeXfih25i6_7nQBPL_K7BFxuyFiKQ",
        "Content-Type": "application/json"
    }
    headers["Authorization"] = "Bearer " + token

    # query_time = 10
    query_time = 1
    add_time = 1

    for i in range(add_time):
        _add_update_delete(headers=headers)

    logging.info(f"Start query, totally {query_time} times.")
    for i in range(query_time):
        _get(headers=headers)
        logging.info(f"Finish query {i+1} / {query_time}")
