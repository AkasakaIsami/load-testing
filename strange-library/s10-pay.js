import http from 'k6/http';

function adminLogin() {
    var url = 'http://10.176.122.80:32677/apiUser/user/login';
    var payload = JSON.stringify({
        password: 'admin',
        username: 'admin',
    });

    var params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    var res = http.post(url, payload, params);

    var str = res.body;
    var obj = eval('(' + str + ')');
    return obj.session;
}

function userLogin() {
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

    var res = http.post(url, payload, params);

    var str = res.body;
    var obj = eval('(' + str + ')');
    return obj.session;
}


export default function () {
    var userSession = userLogin();
    var adminSession = adminLogin();


    var url = 'http://10.176.122.80:32677/apiUser/application/apply';
    var payload = JSON.stringify({
        reason: "zxczc",
        session: `${userSession}`,
    });

    var params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    http.post(url, payload, params);


    http.get('http://10.176.122.80:32677/apiUser/application/');


    url = 'http://10.176.122.80:32677/apiUser/application/approve';
    payload = JSON.stringify({
        username: "20212010138",
        session: `${adminSession}`,
    });



    http.post(url, payload, params);

    http.get('http://10.176.122.80:32677/apiUser/application/');


}