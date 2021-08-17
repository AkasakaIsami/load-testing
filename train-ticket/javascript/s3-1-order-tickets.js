import http from 'k6/http';
import {
    TOKEN
} from './config.js';

export let options = {
    vus: 1,
    iterations: 2,
};

export default function () {
console.log(TOKEN);
    var params = {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `${TOKEN}`,
        },
    };

    http.get('http://10.176.122.1:32677/api/v1/assuranceservice/assurances/types', params);
    http.get('http://10.176.122.1:32677/api/v1/foodservice/foods/2021-08-16/Shang%20Hai/Su%20Zhou/D134', params);
    http.get('http://10.176.122.1:32677/api/v1/contactservice/contacts/account/4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f', params);


    var url = 'http://10.176.122.1:32677/api/v1/preserveservice/preserve';

    var payload = JSON.stringify({
        accountId: '4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f',
        assurance: '1',
        contactsId: 'f0c9ee5b-25ad-469d-8de1-5d0d41fed495',
        date: '2021-08-16',
        foodName: 'Soup',
        foodPrice: 3.7,
        foodType: 2,
        from: 'Shang Hai',
        seatType: '2',
        stationName: 'suzhou',
        storeName: 'Roman Holiday',
        to: 'Su Zhou',
        tripId: 'D1345',
    });

    http.post(url, payload, params);
}