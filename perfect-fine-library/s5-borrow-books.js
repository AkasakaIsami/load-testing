import http from 'k6/http';
import encoding from 'k6/encoding';


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
    iterations: 10,
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

    url = 'http://10.176.122.80:33004/copies?isbn=2121211171212-001';
    http.get(url, adminParams);

    url = 'http://10.176.122.80:33002/books/1';
    http.get(url, adminParams);

    url = 'http://10.176.122.80:33006/orders?operation=Borrow&copyId=2&username=20212010138';
    http.post(url, payload, adminParams);


    url = 'http://10.176.122.80:33006/orders/1';
    http.get(url, adminParams);



    url = 'http://10.176.122.80:33004/copies?isbn=2121211171212-001';
    http.get(url, adminParams);

    url = 'http://10.176.122.80:33002/books/1';
    http.get(url, adminParams);

    url = 'http://10.176.122.80:33006/orders?operation=Return&copyId=2';
    http.post(url, payload, adminParams);

    url = 'http://10.176.122.80:33006/orders/1';
    http.get(url, adminParams);


};