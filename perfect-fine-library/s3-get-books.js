import http from 'k6/http';

// 用户查询图书


export let options = {
    vus: 1,
    iterations: 10,
};

export default function () {
    var url_getBooks = 'http://10.176.122.80:33677/api/v1/books';
    var url_getBooksWithTitle = 'http://10.176.122.80:33677/api/v1/books?title=wew';

    http.get(url_getBooks);
    http.get(url_getBooksWithTitle);

    http.get('http://10.176.122.80:33677/api/v1/books/2');
    http.get('http://10.176.122.80:33677/api/v1/copies?bookId=2');
    http.get('http://10.176.122.80:33677/api/v1/comments?bookId=2');

}