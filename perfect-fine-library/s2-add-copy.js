import encoding from 'k6/encoding';
import http from 'k6/http';

const username = '00000';
const password = 'keke520';

const credentials = `${username}:${password}`;
const encodedCredentials = encoding.b64encode(credentials);
const options = {
    headers: {
        Authorization: `Basic ${encodedCredentials}`,
    },
};

export default function () {

    var res=http.get('http://10.176.122.80:33677/api/v1/auth/admins/token?library=HD',options);

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
            Authorization: `${res.headers.Authorization}`,
        },
    };

    http.post(url, payload, params);


    var url2 = 'http://10.176.122.80:33677/api/v1/copies';
    var payload2 = JSON.stringify({
        bookId: 2,
        number: 1,
    });

    var res2 = http.post(url2, payload2, params);
    console.log(res2.body);
}