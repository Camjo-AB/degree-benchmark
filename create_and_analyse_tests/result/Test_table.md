# TEST TABLE

## KAFKA

|                     Tests                     | Status | # Pods in Cluster |                                                Comments                                                 |
|:---------------------------------------------:|:------:|:-----------------:|:-------------------------------------------------------------------------------------------------------:|
|               *Throughput_tests               |        |                   |                                                                                                         |
| 0K-rate-100B-size-1-topic-1-partitions-4p-4c  |   OK   |                   |                                                                                                         |
| 0K-rate-500B-size-1-topic-1-partitions-4p-4c  |   OK   |                   |                                                                                                         |
|  0K-rate-1KB-size-1-topic-1-partitions-4p-4c  |   OK   |                   |                                                                                                         |
| 0K-rate-1.5KB-size-1-topic-1-partitions-4p-4c |   OK   |                   |                                                                                                         |
|  0K-rate-2KB-size-1-topic-1-partitions-4p-4c  |   OK   |                   |                                                                                                         |
|  0K-rate-4KB-size-1-topic-1-partitions-4p-4c  |   OK   |                   |                                                                                                         |
| 1K-rate-100B-size-1-topic-1-partitions-4p-4c  |  N/A   |                   |                                                                                                         |
| 1K-rate-500B-size-1-topic-1-partitions-4p-4c  |  N/A   |                   |                                                                                                         |
|  1K-rate-1KB-size-1-topic-1-partitions-4p-4c  |  N/A   |                   |                                                                                                         |
| 1K-rate-1.5KB-size-1-topic-1-partitions-4p-4c |  N/A   |                   |                                                                                                         |
|  1K-rate-2KB-size-1-topic-1-partitions-4p-4c  |  N/A   |                   |                                                                                                         |
|  1K-rate-4KB-size-1-topic-1-partitions-4p-4c  |  N/A   |                   |                                                                                                         |
|                *Latency_tests                 |        |                   |                                                                                                         |
|  1K-rate-1KB-size-1-topic-1-partitions-4p-4c  |   OK   |                   |                                                                                                         |
|  2K-rate-1KB-size-1-topic-1-partitions-4p-4c  |   OK   |                   |                                                                                                         |
|  4K-rate-1KB-size-1-topic-1-partitions-4p-4c  |   OK   |                   |                                                                                                         |
|  6K-rate-1KB-size-1-topic-1-partitions-4p-4c  |   OK   |                   |                                                                                                         |
|  8K-rate-1KB-size-1-topic-1-partitions-4p-4c  |   OK   |                   |                                                                                                         |
| 125-rate-8KB-size-1-topic-1-partitions-4p-4c  |   OK   |                   |                                                                                                         |
| 250-rate-8KB-size-1-topic-1-partitions-4p-4c  |   OK   |                   |                                                                                                         |
| 500-rate-8KB-size-1-topic-1-partitions-4p-4c  |   OK   |                   |                                                                                                         |
| 750-rate-8KB-size-1-topic-1-partitions-4p-4c  |   OK   |                   |                                                                                                         |
|  1K-rate-8KB-size-1-topic-1-partitions-4p-4c  |   OK   |                   |                                                                                                         |
|  2K-rate-8KB-size-1-topic-1-partitions-4p-4c  |   OK   |                   |                                                                                                         |
|  4K-rate-8KB-size-1-topic-1-partitions-4p-4c  |   OK   |                   |                                                                                                         |
|               *Partitions_test                |        |                   |                                                                                                         |
|  0K-rate-1KB-size-1-topic-2-partitions-2p-2c  |   OK   |                   |                                                                                                         |
|  0K-rate-1KB-size-1-topic-4-partitions-4p-4c  |   OK   |                   |                                                                                                         |
|  0K-rate-1KB-size-1-topic-8-partitions-8p-8c  |   OK   |                   |                                                                                                         |
| 0K-rate-1KB-size-1-topic-16-partitions-6p-6c  |        |                   |                                                                                                         |
|  1K-rate-1KB-size-1-topic-2-partitions-2p-2c  |   OK   |                   |                                                                                                         |
|  1K-rate-1KB-size-1-topic-4-partitions-4p-4c  |   OK   |                   |                                                                                                         |
|  1K-rate-1KB-size-1-topic-8-partitions-8p-8c  |   OK   |                   |                                                                                                         |
| 1K-rate-1KB-size-1-topic-16-partitions-6p-6c  |        |                   | 15 Killed                  java -server -cp $CLASSPATH $JVM_MEM io.openmessaging.benchmark.Benchmark $* |
|                 *Topics_tests                 |        |                   |                                                                                                         |
|  OK-rate-1KB-size-1-topic-1-partitions-4p-4c  |        |                   |                                                                                                         |
| OK-rate-1KB-size-100-topic-1-partitions-4p-4c |        |                   |                                                                                                         |
| OK-rate-1KB-size-200-topic-1-partitions-4p-4c |        |                   |                                                                                                         |
| OK-rate-1KB-size-50-topic-1-partitions-4p-4c  |        |                   |                                                                                                         |
| OK-rate-1KB-size-150-topic-1-partitions-4p-4c |        |                   |                                                                                                         |
|  1K-rate-1KB-size-1-topic-1-partitions-4p-4c  |   OK   |                   |                                                                                                         |
| 1K-rate-1KB-size-100-topic-1-partitions-4p-4c |   OK   |                   |                                                                                                         |
| 1K-rate-1KB-size-200-topic-1-partitions-4p-4c |   OK   |                   |                                                                                                         |
| 1K-rate-1KB-size-50-topic-1-partitions-4p-4c  |   OK   |                   |                                                                                                         |
| 1K-rate-1KB-size-150-topic-1-partitions-4p-4c |   OK   |                   |                                                                                                         |
|            *Producer_Consumer_Test            |        |                   |                                                                                                         |
|  0K-rate-1KB-size-1-topic-1-partitions-2p-2c  |        |                   |                                                                                                         |
|  0K-rate-1KB-size-1-topic-1-partitions-4p-4c  |   OK   |                   |                                                                                                         |
|  0K-rate-1KB-size-1-topic-1-partitions-8p-8c  |        |                   |                                                                                                         |
|  0K-rate-1KB-size-1-topic-1-partitions-6p-6c  |        |                   |                                                                                                         |
|  1K-rate-1KB-size-1-topic-1-partitions-2p-2c  |        |                   |                                                                                                         |
|  1K-rate-1KB-size-1-topic-1-partitions-4p-4c  |        |                   |                                                                                                         |
|  1K-rate-1KB-size-1-topic-1-partitions-8p-8c  |        |                   |                                                                                                         |
|  1K-rate-1KB-size-1-topic-1-partitions-6p-6c  |        |                   |                                                                                                         |

## RabbitMQ

|                     Tests                      | Status | # Pods in Cluster |                                         Comments                                          |
|:----------------------------------------------:|:------:|:-----------------:|:-----------------------------------------------------------------------------------------:|
|                                                |        |                   |                                                                                           |
|               *Throughput_tests                |        |                   |                                                                                           |
|  0K-rate-100B-size-1-topic-1-partitions-4p-4c  |   OK   |                   | Rerun from 0K-rate-100B-size-1-topic-1-partitions-4p-4c-RabbitMQ-2024-04-03-10-00-41.json |
|  0K-rate-500B-size-1-topic-1-partitions-4p-4c  |   OK   |                   |   Rerun 0K-rate-500B-size-1-topic-1-partitions-4p-4c-RabbitMQ-2024-04-03-10-10-05.json    |
|  0K-rate-1KB-size-1-topic-1-partitions-4p-4c   |   OK   |                   |       0K-rate-1KB-size-1-topic-1-partitions-4p-4c-RabbitMQ-2024-04-03-10-19-29.json       |
| 0K-rate-1.5KB-size-1-topic-1-partitions-4p-4c  |   OK   |                   |                                                                                           |
|  0K-rate-2KB-size-1-topic-1-partitions-4p-4c   |   OK   |                   |                                                                                           |
|  0K-rate-4KB-size-1-topic-1-partitions-4p-4c   |   OK   |                   |                                                                                           |
|  1K-rate-100B-size-1-topic-1-partitions-4p-4c  |  N/A   |                   |                                                                                           |
|  1K-rate-500B-size-1-topic-1-partitions-4p-4c  |  N/A   |                   |                                                                                           |
|  1K-rate-1KB-size-1-topic-1-partitions-4p-4c   |  N/A   |                   |                                                                                           |
| 1K-rate-1.5KB-size-1-topic-1-partitions-4p-4c  |  N/A   |                   |                                                                                           |
|  1K-rate-2KB-size-1-topic-1-partitions-4p-4c   |  N/A   |                   |                                                                                           |
|  1K-rate-4KB-size-1-topic-1-partitions-4p-4c   |  N/A   |                   |                                                                                           |
|                 *Latency_tests                 |        |                   |                                                                                           |
|  1K-rate-1KB-size-1-topic-1-partitions-4p-4c   |   OK   |                   |                                                                                           |
|  2K-rate-1KB-size-1-topic-1-partitions-4p-4c   |   OK   |                   |                                                                                           |
|  4K-rate-1KB-size-1-topic-1-partitions-4p-4c   |   OK   |                   |                                                                                           |
|  6K-rate-1KB-size-1-topic-1-partitions-4p-4c   |   OK   |                   |                                                                                           |
|  8K-rate-1KB-size-1-topic-1-partitions-4p-4c   |   OK   |                   |                                                                                           |
|  125-rate-8KB-size-1-topic-1-partitions-4p-4c  |   OK   |                   |                                                                                           |
|  250-rate-8KB-size-1-topic-1-partitions-4p-4c  |   OK   |                   |                                                                                           |
|  500-rate-8KB-size-1-topic-1-partitions-4p-4c  |   OK   |                   |                                                                                           |
|  750-rate-8KB-size-1-topic-1-partitions-4p-4c  |   OK   |                   |                                                                                           |
|  1K-rate-8KB-size-1-topic-1-partitions-4p-4c   |   Ok   |                   |                                                                                           |
|  2K-rate-8KB-size-1-topic-1-partitions-4p-4c   |   OK   |                   |                                                                                           |
|  4K-rate-8KB-size-1-topic-1-partitions-4p-4c   |   OK   |                   |                                                                                           |
|                *Partitions_test                |        |                   |                                                                                           |
|  0K-rate-1KB-size-1-topic-2-partitions-2p-2c   |  N/A   |                   |                                                                                           |
|  0K-rate-1KB-size-1-topic-4-partitions-4p-4c   |  N/A   |                   |                                                                                           |
|  0K-rate-1KB-size-1-topic-8-partitions-8p-8c   |  N/A   |                   |                                                                                           |
| 0K-rate-1KB-size-1-topic-16-partitions-16p-16c |  N/A   |                   |                                                                                           |
|  1K-rate-1KB-size-1-topic-2-partitions-2p-2c   |  N/A   |                   |                                                                                           |
|  1K-rate-1KB-size-1-topic-4-partitions-4p-4c   |  N/A   |                   |                                                                                           |
|  1K-rate-1KB-size-1-topic-8-partitions-8p-8c   |  N/A   |                   |                                                                                           |
|  1K-rate-1KB-size-1-topic-16-partitions-6p-6c  |  N/A   |                   |                                                                                           |
|                 *Topics_tests                  |        |                   |                                                                                           |
|  0K-rate-1KB-size-1-topic-1-partitions-4p-4c   |  N/A   |                   |                                                                                           |
| 0K-rate-1KB-size-100-topic-1-partitions-4p-4c  |  N/A   |                   |                                                                                           |
| 0K-rate-1KB-size-200-topic-1-partitions-4p-4c  |  N/A   |                   |                                                                                           |
|  0K-rate-1KB-size-50-topic-1-partitions-4p-4c  |  N/A   |                   |                                                                                           |
| 0K-rate-1KB-size-150-topic-1-partitions-4p-4c  |  N/A   |                   |                                                                                           |
|  1K-rate-1KB-size-1-topic-1-partitions-4p-4c   |  N/A   |                   |                                                                                           |
| 1K-rate-1KB-size-100-topic-1-partitions-4p-4c  |  N/A   |                   |                                                                                           |
| 1K-rate-1KB-size-200-topic-1-partitions-4p-4c  |  N/A   |                   |                                                                                           |
|  1K-rate-1KB-size-50-topic-1-partitions-4p-4c  |  N/A   |                   |                                                                                           |
| 1K-rate-1KB-size-150-topic-1-partitions-4p-4c  |  N/A   |                   |                                                                                           |
|            *Producer_Consumer_Test             |        |                   |                                                                                           |
|  0K-rate-1KB-size-1-topic-1-partitions-2p-2c   |        |                   |                                                                                           |
|  0K-rate-1KB-size-1-topic-1-partitions-4p-4c   |   OK   |                   |                                                                                           |
|  0K-rate-1KB-size-1-topic-1-partitions-8p-8c   |        |                   |                                                                                           |
|  0K-rate-1KB-size-1-topic-1-partitions-6p-6c   |        |                   |                                                                                           |
|  1K-rate-1KB-size-1-topic-1-partitions-2p-2c   |        |                   |                                                                                           |
|  1K-rate-1KB-size-1-topic-1-partitions-4p-4c   |        |                   |                                                                                           |
|  1K-rate-1KB-size-1-topic-1-partitions-8p-8c   |        |                   |                                                                                           |
|  1K-rate-1KB-size-1-topic-1-partitions-6p-6c   |        |                   |                                                                                           |

