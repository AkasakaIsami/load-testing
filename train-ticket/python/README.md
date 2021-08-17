# train-ticket-auto-query
Train Ticket Auto Query Python Scripts



### 1 Scenrios defination

| Scenrio | Description                   | Frequency | Python script                                                | Invocation times in script |
| ------- | ----------------------------- | --------- | ------------------------------------------------------------ | -------------------------- |
| S1      | login                         | 1         | This operation is included in any other scenrio.             | —                          |
| S2      | query tickets                 | 10        | query_tickets.py<br />Also this operation is included in any other S4. | 1000                       |
| S3      | advanced query tickets        | 10        | query_advanced_ticket.py                                     | 200                        |
| S4      | order tickets                 | 3         | query_and_preserve.py                                        | 1000                       |
| S5      | query orders                  | 5         | This operation is included in any other scenrio.             | —                          |
| S6      | pay                           | 3         | query_order_and_pay.py                                       | 1                          |
| S7      | update consign info           | 3         | query_and_update_consign.py                                  | 1                          |
| S8      | rebook                        | 1         | query_and_rebook.py                                          | 1                          |
| S9      | cancel order                  | 1         | query_and_cancel.py                                          | 1                          |
| S10     | query and update consign info | 5         | query_consign.py                                             | 1                          |
| S11     | collect tickets               | 1         | query_and_collect_ticket.py                                  | 1                          |
| S12     | enter stations                | 1         | query_and_enter_station.py                                   | 1                          |





