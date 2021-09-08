# train-ticket load testing script
train-ticket load testing js scripts for K6

Including only the admin querying station operation in Train Ticket for the two third part metrics. To run the scripts, run the code below in shell in current working directory:

```shell
k6 run --http-debug admin-query-station.js
```

