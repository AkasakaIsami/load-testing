import http from 'k6/http';
import "./config/config.js";

export default function () {
    var url = 'http://10.176.122.80:33677/api/v1/auth/users/verification_id';
    var payload = JSON.stringify({
        username: '20212010138',
        password: 'fdse123123',
        role: 'POSTGRADUATE',
    });

    var params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    const res = http.post(url, payload, params);
    console.log(res.body.JSON);


}