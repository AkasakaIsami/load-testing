import http from 'k6/http';

// 管理员登录 加书加副本 改借书时间上限

export default function () {
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
    typeof (obj)


    url = 'http://10.176.122.80:32677/apiBook/book/copy/add/';
    payload = JSON.stringify({
        ISBN: "1111111111111",
        location: "邯郸",
        number: 5,
        session: `${obj.session}`,
    });


    http.post(url, payload, params);

    http.get('http://10.176.122.80:32677/apiBook/book/copy/getCopyByIsbn/1111111111111');

    http.get('http://10.176.122.80:32677/apiBorrow/borrowRules');


    url = 'http://10.176.122.80:32677/apiBorrow/borrowRules';
    payload = JSON.stringify({
        borrowTimePostgra: "30000",
        borrowTimeTeacher: 30,
        borrowTimeUndergra: 30,
        maxAmountPostgra: 50,
        maxAmountTeacher: 5,
        maxAmountUndergra: 5,
        subscribeTimePostgra: "30000",
        subscribeTimeTeacher: 30,
        subscribeTimeUndergra: 30,
    });


    http.post(url, payload, params);

}