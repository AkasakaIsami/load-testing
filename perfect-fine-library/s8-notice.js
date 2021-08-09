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

export default function () {
    var url;

    var adminParams = {
        headers: {
            'Content-Type': 'application/json',
            Authorization: `${adminLogin()}`,
        },
    };

    url = 'http://10.176.122.80:33006/orders?username=';
    http.get(url, adminParams);

    url = 'http://10.176.122.80:33001/admin/notify';
    http.get(url, adminParams);
}
