import http from 'k6/http';

// 用户查询图书


export let options = {
    vus: 1,
    iterations: 10,
};

export default function () {
    var url_getBooks = 'http://10.176.122.80:32677/apiBook/book/get/browse';
    var url_getBooksWithTitle = 'http://10.176.122.80:32677/apiBook/book/get/title/soft';

    var payload = JSON.stringify({});

    var params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    http.post(url_getBooks, payload, params);
    http.post(url_getBooksWithTitle, payload, params);


    http.get('http://10.176.122.80:32677/apiComment/comment/isbn/1111111111111');
    http.post('http://10.176.122.80:32677/apiBook/book/get/ISBN/1111111111111', payload, params);
    http.get('http://10.176.122.80:32677/apiBook/book/copy/getCopyByIsbn/1111111111111');
    http.get('http://10.176.122.80:32677/apiComment/comment/isbn/1111111111111');


}