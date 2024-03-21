# Tested workloads

The following are the tested workloads divided over two message brokers under test. All test in AKS Cluster.

## Messasge broker

### RabbitMQ

| Workload                             |   Status    | # pods in cluster |                                                                                       Comment                                                                                        |
|:-------------------------------------|:-----------:|:-----------------:|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| 1-topic-1-partition-1kb              |   Working   |         2         |                                                    Works only with cluster of two workers. <br/>One publisher and one subscriber.                                                    |
| 1-topic-1-partitions-1kb-4p-4c-50k   |             |                   |                                                                                                                                                                                      |
| PRODUCER RATE TESTS                  |             |                   |                                                                                                                                                                                      |
| 1-topic-1-partitions-1kb-4p-4c-50k   |   Working   |         8         |                                                                      Was possible to run without reinstallation                                                                      |
| 1-topic-1-partitions-1kb-4p-4c-100k  |   Working   |         8         |                                                                      Was possible to run without reinstallation                                                                      |
| 1-topic-1-partitions-1kb-4p-4c-150k  |   Working   |         8         |                                                                      Was possible to run without reinstallation                                                                      |
| 1-topic-1-partitions-1kb-4p-4c-200k  |   Working   |         8         | Symptom: benchmark-driver freezes <br/> See log in benchmark-worker-7-1-topic-1-partitions-1kb-4p-4c-500k.yaml.txt <br/> Fix: by uninstalling benchmark-application and reinstalling |
| 1-topic-1-partitions-1kb-4p-4c-500k  |   Working   |         8         |                                                                                      See above                                                                                       |
| 1-topic-1-partitions-1kb-4p-4c-1000k |   Working   |         8         |                                                                          Was possible to run from beginning                                                                          |
| 1-topic-1-partitions-1kb-4p-4c-1500k |   Working   |         8         |                                                                                                                                                                                      |
| 1-topic-1-partitions-1kb-4p-4c-2000k |   Working   |         8         |                                                                                                                                                                                      |
| MESSAGE SIZE TESTS                   |             |                   |                                                                                                                                                                                      |
| 1-topic-1-partitions-2kb-4p-4c-50k   |   Working   |         8         |                                                                                                                                                                                      |
| 1-topic-1-partitions-4kb-4p-4c-50k   | Not Working |         8         |                                                            See benchmark-worker-1-1-topic-1-partitions-4kb-4p-4c-50k.yaml                                                            |
| 1-topic-1-partitions-100b-4p-4c-50k  |   Working   |         8         |                                                                                                                                                                                      |
| 1-topic-1-partitions-200b-4p-4c-50k  |   Working   |         8         |                                                                                                                                                                                      |
| 1-topic-1-partitions-400b-4p-4c-50k  |   Working   |         8         |                                                                                                                                                                                      |
| 1-topic-1-partitions-600b-4p-4c-50k  |   Working   |         8         |                                                                                                                                                                                      |
| 1-topic-1-partitions-800b-4p-4c-50k  |   Working   |         8         |                                                                                                                                                                                      |
| PRODUCER / CONSUMER TEST             |             |                   |                                                                                                                                                                                      |
| 1-topic-1-partitions-1kb-2p-2c-50k   |             |         4         |                                                   Works only with cluster of four workers. <br/>Two publisher and two subscriber.                                                    |
| 1-topic-1-partitions-1kb-8p-8c-50k   |             |        16         |                                                                                                                                                                                      |
| 1-topic-1-partitions-1kb-16p-16c-50k |             |        32         |                                                                                                                                                                                      |

### Kafka

| Workload                                    | Status  | # pods in cluster |                                                Comment                                                 |
|:--------------------------------------------|:-------:|:-----------------:|:------------------------------------------------------------------------------------------------------:|
| 1-topic-1-partition-1kb                     | Working |         8         |                                   Works no matter number of workers                                    |
| 1-topic-100-partitions-1kb-4p-4c-200k       | Working |         8         |                                       Work by 8 default workers                                        |
| max-rate-20-topics-1-partition-1kb.yaml     | Working |         8         |                                                                                                        |
| max-rate-1-topic-16-partitions-1kb.yaml     | Working |         8         |                                                                                                        |
| max-rate-1-topic-1-partition-4p-1c-1kb.yaml | Working |         8         |                                                                                                        |
| PRODUCER RATE TESTS                         |         |                   |                                                                                                        |
| 1-topic-1-partitions-1kb-4p-4c-50k          | Working |         8         | All testing with kafka will require restart of cluster<br/>Having problem memory saturation of cluster |
| 1-topic-1-partitions-1kb-4p-4c-100k         | Working |         8         |                              Having problem memory saturation of cluster                               |
| 1-topic-1-partitions-1kb-4p-4c-150k         | Working |         8         |                              Having problem memory saturation of cluster                               |
| 1-topic-1-partitions-1kb-4p-4c-200k         | Working |         8         |                 Tesing with kafka-ephemeral-modified including request and limits set                  |
| 1-topic-1-partitions-1kb-4p-4c-500k         | Working |         8         |                                                                                                        |
| 1-topic-1-partitions-1kb-4p-4c-1000k        | Working |         8         |                                                                                                        |
| 1-topic-1-partitions-1kb-4p-4c-1500k        | Working |         8         |                                                                                                        |
| 1-topic-1-partitions-1kb-4p-4c-2000k        | Working |         8         |                                                                                                        |
| MESSAGE SIZE TESTS                          |         |                   |                                                                                                        |
| 1-topic-1-partitions-2kb-4p-4c-50k          | Working |         8         |                                                                                                        |
| 1-topic-1-partitions-4kb-4p-4c-50k          | Working |         8         |                                                                                                        |
| 1-topic-1-partitions-100b-4p-4c-50k         | Working |         8         |                                                                                                        |
| 1-topic-1-partitions-200b-4p-4c-50k         | Working |         8         |                                                                                                        |
| 1-topic-1-partitions-400b-4p-4c-50k         | Working |         8         |                                                                                                        |
| 1-topic-1-partitions-600b-4p-4c-50k         | Working |         8         |                                                                                                        |
| 1-topic-1-partitions-800b-4p-4c-50k         | Working |         8         |                                                                                                        |
| PRODUCER / CONSUMER TEST                    |         |                   |                                                                                                        |
| 1-topic-1-partitions-1kb-2p-2c-50k          |         |         4         |                                                                                                        |
| 1-topic-1-partitions-1kb-8p-8c-50k          |         |        16         |                                                                                                        |
| 1-topic-1-partitions-1kb-16p-16c-50k        |         |        32         |                                                                                                        |
| PARTITIONS                                  |         |                   |                                                                                                        |
| 1-topic-10-partitions-1kb-4p-4c-100k.yaml   | Working |         8         |                                                                                                        |
| 1-topic-50-partitions-1kb-4p-4c-100k.yaml   | Working |         8         |                                                                                                        |
| 1-topic-100-partitions-1kb-4p-4c-100k.yaml  | Working |         8         |                                                                                                        |
| TOPICS                                      |         |                   |                                                                                                        |
| 100-topic-1kb-4p-4c-100k.yaml               | Working |         8         |                                                                                                        |
| 80-topic-1kb-4p-4c-100k.yaml                |         |         8         |                                                                                                        |
| 60-topic-1kb-4p-4c-100k.yaml                |         |         8         |                                                                                                        |
| 40-topic-1kb-4p-4c-100k.yaml                |         |         8         |                                                                                                        |
| 20-topic-1kb-4p-4c-100k.yaml                |         |         8         |                                                                                                        |
