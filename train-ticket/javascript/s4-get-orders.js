import http from 'k6/http';
import {
    TOKEN
} from './config.js';

export let options = {
    vus: 1,
    iterations: 5,
};

export default function () {
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

    http.post(url, payload, params);

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
    http.post(url, payload, params);

}