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
    var res = http.get('http://10.176.122.80:33677/api/v1/auth/users/token', userOptions);
    return res.headers.Authorization;
}

export let options = {
    vus: 1,
    iterations: 5,
};

export default function () {
    var userParams = {
        headers: {
            'Content-Type': 'application/json',
            Authorization: `${userLogin()}`,
        },
    };
    var url;
    var payload = JSON.stringify({
        commentId: 1,
        content: "I like it.",
        toId: null,
    });

    url = 'http://10.176.122.80:33003/comments/1/replies';
    http.post(url, payload, userParams);
    
}