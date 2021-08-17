import http from 'k6/http';

var TOKEN="";
export let options = {
    vus: 1,
    iterations: 1,
};

export default function () {
    var url = 'http://10.176.122.1:32677/api/v1/users/login';

    var payload = JSON.stringify({
        password: "111111",
        username: "fdse_microservice",
        verificationCode: "1234",
    });

    var params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    var res = http.post(url, payload, params);

    TOKEN = "Bearer "+json2obj(res).data.token;
    console.log(TOKEN);
}

function json2obj(res) {
    var str = res.body;
    var obj = eval('(' + str + ')');
    return obj;
}

export {
    TOKEN
}