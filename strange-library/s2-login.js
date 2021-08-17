import http from 'k6/http';

export let options = {
    vus: 1,
    iterations: 5,
};

export default function () {
    var url = 'http://10.176.122.80:32677/apiUser/user/login';
    var payload = JSON.stringify({
        password: 'fdse123123',
        username: '20212010138',
    });

    var params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    http.post(url, payload, params);
}