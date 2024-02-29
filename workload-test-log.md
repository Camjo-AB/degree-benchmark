# Tested workloads

The following are the tested workloads divided over two message brokers under test. All test in AKS Cluster.

## Messasge broker

### RabbitMQ

| Workload                              | Status  | # pods in cluster |                                                                         Comment |
|:--------------------------------------|:-------:|:-----------------:|--------------------------------------------------------------------------------:|
| 1-topic-1-partition-1kb               | Working |         2         |  Works only with cluster of two workers. <br/>One publisher and one subscriber. |
| 1-topic-1-partitions-1kb-2p-2c-50k    | Working |         4         | Works only with cluster of four workers. <br/>Two publisher and two subscriber. |
| 1-topic-100-partitions-1kb-4p-4c-200k |         |                   |
|                                       |         |                   |

### Kafka

| Workload                              | Status  | # pods in cluster |                           Comment |
|:--------------------------------------|:-------:|:-----------------:|----------------------------------:|
| 1-topic-1-partition-1kb               | Working |         8         | Works no matter number of workers |
| 1-topic-100-partitions-1kb-4p-4c-200k | Working |         8         |         Work by 8 default workers |
|                                       |         |                   |                                   | 
|                                       |         |                   |                                   |

