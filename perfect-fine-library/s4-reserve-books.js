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



// 管理员登录
const adminUsername = '00000';
const adminPassword = 'keke520';

const adminCredentials = `${adminUsername}:${adminPassword}`;
const adminEncodedCredentials = encoding.b64encode(adminCredentials);
const adminOptions = {
    headers: {
        Authorization: `Basic ${adminEncodedCredentials}`,
    },
};

function adminLogin() {
    var res = http.get('http://10.176.122.80:33000/auth/admins/token?library=HD', adminOptions);
    return res.headers.Authorization;
}


export let options = {
    vus: 1,
    iterations: 5,
};

export default function () {


    var url;
    var payload = JSON.stringify({});

    var adminParams = {
        headers: {
            'Content-Type': 'application/json',
            Authorization: `${adminLogin()}`,
        },
    };

    var userParams = {
        headers: {
            'Content-Type': 'application/json',
            Authorization: `${userLogin()}`,
        },
    };

    url = 'http://10.176.122.80:33006/orders?operation=Reserve&copyId=1';
    http.post(url, payload, userParams);

    url = 'http://10.176.122.80:33006/orders/1';
    http.get(url, userParams);

    http.get('http://10.176.122.80:33004/copies?username=20212010138&status=Reserved', adminParams)

    url = 'http://10.176.122.80:33002/books/1';
    http.get(url, adminParams);

    url = 'http://10.176.122.80:33006/orders?operation=Borrow&copyId=1&username=20212010138';
    http.post(url, payload, adminParams);

    url = 'http://10.176.122.80:33006/orders/2';
    http.get(url, adminParams);

    url = 'http://10.176.122.80:33004/copies?isbn=2121211171212-000';
    http.get(url, adminParams);

    url = 'http://10.176.122.80:33002/books/1';
    http.get(url, adminParams);

    url = 'http://10.176.122.80:33006/orders?operation=Return&copyId=1';
    http.post(url, payload, adminParams);

    url = 'http://10.176.122.80:33006/orders/3';
    http.get(url, adminParams);
}