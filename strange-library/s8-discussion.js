import http from 'k6/http';

export let options = {
    vus: 1,
    iterations: 5,
};

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
    var url = 'http://10.176.122.80:32677/apiComment/comment/isbn/1111111111111';
    var res = http.get(url);

    var str = res.body;
    var obj = eval('(' + str + ')');
    var id =obj.comments[0].id;


    url = 'http://10.176.122.80:32677/apiComment/discussion/release/';
    var payload = JSON.stringify({
        commentId: `${id}`,
        content: "adfafadf",
        session: `${userSession}`,
    });

    var params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };
    http.post(url, payload, params);

    url = 'http://10.176.122.80:32677/apiComment/comment/isbn/1111111111111';
    http.get(url);

}