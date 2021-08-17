import http from 'k6/http';

export default function () {
    http.get('http://10.176.122.80:32677/apiLog/logger/getAll/');

    var url = 'http://10.176.122.80:32677/apiViolation/broadcast';
    var payload = JSON.stringify({
    });

    var params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    http.post(url, payload, params);

}