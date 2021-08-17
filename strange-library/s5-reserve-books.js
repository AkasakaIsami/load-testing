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


export let options = {
    vus: 1,
    iterations: 5,
};

export default function () {


    var userSession = userLogin();
    var adminSession = adminLogin();

    var url;
    var payload = JSON.stringify({
        copyId: "1111111111111-001",
        session: `${userSession}`,
    });

    var params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    url = 'http://10.176.122.80:32677/apiBorrow/borrow/reserve';
    http.post(url, payload, params);

    http.get('http://10.176.122.80:32677/apiBook/book/copy/getCopyByIsbn/1111111111111');


    url = 'http://10.176.122.80:32677/apiBook/book/copy/userReserved/';
    payload = JSON.stringify({
        branch: "邯郸",
        username: "20212010138",
    });
    http.post(url, payload, params);

    url = 'http://10.176.122.80:32677/apiBorrow/borrow/getReserve';
    payload = JSON.stringify({
        borrower: "20212010138",
        branch: "邯郸",
        copyId: "1111111111111-001",
        session: `${adminSession}`,
    });
    http.post(url, payload, params);

    url = 'http://10.176.122.80:32677/apiBook/book/copy/userReserved/';
    payload = JSON.stringify({
        branch: "邯郸",
        username: "20212010138",
    });
    http.post(url, payload, params);



    url = 'http://10.176.122.80:32677/apiBorrow/borrow/onsiteReturn';
    payload = JSON.stringify({
        branch: "邯郸",
        copyId: "1111111111111-001",
        session: `${adminSession}`,
        status: "完好",
    });
    http.post(url, payload, params);


}