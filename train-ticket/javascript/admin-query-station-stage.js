import http from 'k6/http';
import {
    base_addr,
} from './config.js';
import {
    json2obj
} from './utils.js';
import {
    check
} from 'k6';

export let options = {
    scenarios: {
      contacts: {
        executor: 'ramping-arrival-rate',
        startRate: 0,
        timeUnit: '1s',
        preAllocatedVUs: 50,
        maxVUs: 100,
        stages: [
          { target: 4, duration: '15s' },
          { target: 4, duration: '10s' },
          { target: 0, duration: '15s' },
        ],
      },
    },
  };
  
export function setup() {
    var url = base_addr + '/api/v1/users/login';

    var payload = JSON.stringify({
        password: "222222",
        username: "admin",
        verificationCode: "1234",
    });

    var params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    var res = http.post(url, payload, params);

    // console.log(JSON.stringify(res))
    if (res.status == 200) {
        var TOKEN = "Bearer " + json2obj(res.body).data.token;
        console.log("Login success.");
        console.log("Authorization: " + TOKEN);
        return TOKEN;
    } else {
        console.log("Login fail.");
        return null;
    }
}


export default function (data) {
    var url = base_addr + '/api/v1/adminbasicservice/adminbasic/stations';

    var params = {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `${data}`,
        },
    };

    let res = http.get(url, params);

    check(res, {
        'is status 200': (r) => r.status === 200,
    });

    if (res.status == 200) {
        var len = json2obj(res.body).data.length;
        console.log("Get stations success, totally " + len + " stations.");
    } else
        console.log("Query fail.");
}