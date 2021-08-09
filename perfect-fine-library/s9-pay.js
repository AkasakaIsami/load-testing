import http from 'k6/http';
import encoding from 'k6/encoding';

// 用户登录
const username = '20212010138';
const password = 'fdse123123';

const credentials = `${username}:${password}`;
const encodedCredentials = encoding.b64encode(credentials);
const userOptions = {
    headers: {
        Authorization: `Basic ${encodedCredentials}`,
    },
};

function userLogin() {
    var res = http.get('http://10.176.122.80:33007/auth/users/token', userOptions);
    return res.headers.Authorization;
}

export default function () {

    var url;

    var userParams = {
        headers: {
            'Content-Type': 'application/json',
            Authorization: `${userLogin()}`,
        },
    };

    url = 'http://10.176.122.80:33008/api/v1/users/my';
    http.get(url, userParams);

    url = 'http://10.176.122.80:33008/users/pay_fine';
    http.get(url, userParams);
}