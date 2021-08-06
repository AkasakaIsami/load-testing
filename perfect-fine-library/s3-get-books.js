import http from 'k6/http';

export let options = {
    vus: 10,
    duration: '5s',
};

export default function () {
    var url_getBooks = 'http://10.176.122.80:33677/api/v1/books';
    var url_getBooksWithTitle = 'http://10.176.122.80:33677/api/v1/books?title=wew';

    http.get(url_getBooks);
    http.get(url_getBooksWithTitle);
}