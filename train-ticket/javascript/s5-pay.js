import http from 'k6/http';
import {
    TOKEN
} from './config.js';

export let options = {
    vus: 1,
    iterations: 2,
};

function json2obj(res) {
    var str = res.body;
    var obj = eval('(' + str + ')');
    return obj;
}

export default function () {
    var order1;
    var order2;
    var trip1;
    var trip2;
    var url = 'http://10.176.122.1:32677/api/v1/orderservice/order/refresh';

    var payload = JSON.stringify({
        boughtDateEnd: null,
        boughtDateStart: null,
        enableBoughtDateQuery: false,
        enableStateQuery: false,
        enableTravelDateQuery: false,
        loginId: '4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f',
        travelDateEnd: null,
        travelDateStart: null,
    });

    var params = {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `${TOKEN}`,
        },
    };

    var res1 = http.post(url, payload, params);
    var orders = json2obj(res1).data;

    for (var j = 0, len = orders.length; j < len; j++) {
        if (orders[j].status == 0) {
            order1 = orders[j].id;
            trip1 = orders[j].trainNumber;
            console.log("found:" + order1 + " " +trip1);

            break;
        }
    }

    url = 'http://10.176.122.1:32677/api/v1/orderOtherService/orderOther/refresh';

    payload = JSON.stringify({
        boughtDateEnd: null,
        boughtDateStart: null,
        enableBoughtDateQuery: false,
        enableStateQuery: false,
        enableTravelDateQuery: false,
        loginId: '4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f',
        travelDateEnd: null,
        travelDateStart: null,
    });

    var res2 = http.post(url, payload, params);
    orders = json2obj(res2).data;

    for (var j = 0, len = orders.length; j < len; j++) {
        if (orders[j].status == 0) {
            order2 = orders[j].id;
            trip2 = orders[j].trainNumber;
            console.log("found:" + order2 + " " +trip2);
            break;
        }
    }

    url = 'http://10.176.122.1:32677/api/v1/inside_pay_service/inside_payment';

    payload = JSON.stringify({
        orderId: `${order1}`,
        tripId: `${trip1}`
    });

    http.post(url, payload, params);

    payload = JSON.stringify({
        orderId: `${order2}`,
        tripId: `${trip2}`
    });

    http.post(url, payload, params);

}