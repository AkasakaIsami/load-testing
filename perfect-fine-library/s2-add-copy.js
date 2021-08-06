import encoding from 'k6/encoding';
import http from 'k6/http';


// 管理员登录 加书加副本 改借书时间上限


const username = '00000';
const password = 'keke520';

const credentials = `${username}:${password}`;
const encodedCredentials = encoding.b64encode(credentials);
const options = {
    headers: {
        Authorization: `Basic ${encodedCredentials}`,
    },
};

function adminLogin() {
    var res = http.get('http://10.176.122.80:33677/api/v1/auth/admins/token?library=HD', options);
    return res.headers.Authorization;
}

export default function () {

    var url = 'http://10.176.122.80:33677/api/v1/books';
    var payload = JSON.stringify({
        author: "weasdasdaq",
        brief: "qwe2112",
        cover: "https://kaola-pop.oss.kaolacdn.com/b74225de-1d74-4346-9338-44aab05df0d5.jpg",
        isbn: "2121211171212",
        library: "",
        price: "12",
        publicationDate: "2021-01-31T16:00:00.000Z",
        title: "qweqwdwq",
    });


    var params = {
        headers: {
            'Content-Type': 'application/json',
            Authorization: `${adminLogin()}`,
        },
    };

    http.post(url, payload, params);


    var url2 = 'http://10.176.122.80:33677/api/v1/copies';
    var payload2 = JSON.stringify({
        bookId: 1,
        number: 5,
    });

    var res2 = http.post(url2, payload2, params);
    console.log(res2.body);

    var url3 = 'http://10.176.122.80:33677/api/v1/admin/configs';
    var payload3 = '[{"maxBorrowNumber":10,"borrowExpiration":60000,"reserveExpiration":60000,"role":"UNDERGRADUATE"},{"maxBorrowNumber":5,"borrowExpiration":18060000,"reserveExpiration":18060000,"role":"POSTGRADUATE"},{"maxBorrowNumber":1,"borrowExpiration":60000,"reserveExpiration":60000,"role":"TEACHER"}]'

    http.put(url3, payload3, params);



}