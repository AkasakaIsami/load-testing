import http from 'k6/http';
import {
    TOKEN
} from './config.js';

export let options = {
    vus: 1,
    iterations: 2,
};

export default function () {

    var params = {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `${TOKEN}`,
        },
    };

    http.get('http://10.176.122.1:32677/api/v1/assuranceservice/assurances/types', params);
    http.get('http://10.176.122.1:32677/api/v1/foodservice/foods/2022-09-16/Shang%20Hai/Nan%20Jing/Z1234', params);
    http.get('http://10.176.122.1:32677/api/v1/contactservice/contacts/account/4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f', params);


    var url = 'http://10.176.122.1:32677/api/v1/preserveotherservice/preserveOther';

    var payload = JSON.stringify({
        accountId: '4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f',
        assurance: '1',
        consigneeName: "test",
        consigneePhone: "11188811111",
        consigneeWeight: 12,
        contactsId: 'f0c9ee5b-25ad-469d-8de1-5d0d41fed495',
        date: '2021-08-16',
        foodName: 'Bone Soup',
        foodPrice: 2.5,
        foodType: 1,
        from: 'Shang Hai',
        handleDate: "2021-08-16",
        isWithin: false,
        seatType: '2',
        stationName: '',
        storeName: '',
        to: 'Nan Jing',
        tripId: 'Z1234',
    });

    http.post(url, payload, params);
}