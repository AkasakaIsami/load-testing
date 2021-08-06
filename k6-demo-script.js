import http from 'k6/http';
import {
  check,
  sleep
} from 'k6';

export let options = {
  vus: 10,
  duration: '1s',
};

export default function () {
  console.log("hi");
}