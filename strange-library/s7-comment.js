import http from 'k6/http';

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
    var url = 'http://10.176.122.80:32677/apiComment/comment/getBySession/' + `${userSession}`;
    var res = http.get(url);

    var str = res.body;
    var obj = eval('(' + str + ')');
    var id =obj.comments[0].id;

    url = 'http://10.176.122.80:32677/apiComment/comment/make/';
    var payload = JSON.stringify({
        comment: "zhenbucuo",
        id: `${id}`,
        rate: 5,
        title: "zhenbucuo",
    });

    var params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };
    http.post(url, payload, params);

    url = 'http://10.176.122.80:32677/apiComment/comment/getBySession/' + `${userSession}`;
    http.get(url);

}