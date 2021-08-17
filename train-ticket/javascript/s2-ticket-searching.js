import http from 'k6/http';
import {
  TOKEN
} from './config.js';

export let options = {
  vus: 1,
  iterations: 10,
};

export default function () {
  var url = 'http://10.176.122.1:32677/api/v1/travelservice/trips/left';

  var payload = JSON.stringify({
    startingPlace: 'Shang Hai',
    endPlace: 'Su Zhou',
    departureTime: '2022-01-04',
  });

  var params = {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `${TOKEN}`,
    },
  };

  http.post(url, payload, params);

  url = 'http://10.176.122.1:32677/api/v1/travel2service/trips/left';

  payload = JSON.stringify({
    startingPlace: 'Shang Hai',
    endPlace: 'Nan Jing',
    departureTime: '2022-01-04',
  });
  http.post(url, payload, params);

}