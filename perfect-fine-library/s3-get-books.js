import http from 'k6/http';

// 用户查询图书


export let options = {
    vus: 1,
    iterations: 10,
};

export default function () {
    var url_getBooks = 'http://10.176.122.80:33002/books';
    var url_getBooksWithTitle = 'http://10.176.122.80:33002/books?title=wew';

    http.get(url_getBooks);
    http.get(url_getBooksWithTitle);

    http.get('http://10.176.122.80:33002/books/1');
    http.get('http://10.176.122.80:33004/copies?bookId=1');
    http.get('http://10.176.122.80:33003/comments?bookId=1');

}