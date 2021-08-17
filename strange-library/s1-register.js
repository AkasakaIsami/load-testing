import http from 'k6/http';

export default function () {
    http.get('http://10.176.122.80:32677/apiUser/user/captcha/20212010138');


    var url = 'http://10.176.122.80:32677/apiUser/user/register/';
    var payload = JSON.stringify({
        captcha: 'TODO',
        password: 'fdse123123',
        username: '20212010138',
    });

    var params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    http.post(url, payload, params);

    url = 'http://10.176.122.80:32677/apiBook/book/get/browse';

    http.post(url, params);

}