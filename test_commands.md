### Creat secrete

kubectl create secret generic regcred --from-file=.dockerconfigjson="\.docker\config.json" --type=kubernetes.io/dockerconfigjson

password="password"
username="username"

echo "username: $username"
echo "password: $password"

kubectl create secret docker-registry regcred --docker-server="https://index.docker.io/v1/" --docker-username="$username" --docker-password="$password" --docker-email="email"

# Miscellaneous commands minikube & kubectlkbue

----------------------------------------------

### Minikube create minikube cluster

minikube start -p kafka --cpus=4 --memory=4096
minikube start -p kafka --cpus=4 --memory=6144

### Switch cluster on minikube

minikube profile kafka

### Set context

kubectl config use-context degree_v1

### Get namespaces

kubectl config get-contexts

### Copy file from pod to local

kubectl cp driver-rabbitmq/new_rabbitmq.yaml benchmark-driver:/benchmark/driver-rabbitmq

### Check pod status

kubectl get pods -o wide

### Check and Change current namespace

kubectl get namespaces
kubectl config set-context --current --namespace=<insert-namespace-name-here>

### Access Benchmark driver CLI

kubectl exec -ti benchmark-driver -- //bin/bash

### Get logs

kubectl logs benchmark-worker-7 > ./result/benchmark-worker-7.txt

### Install benchmark application

helm install benchmark ./deployment/kubernetes/helm/benchmark

kubectl port-forward benchmark-worker-0 80:8080

### Port-forward Kafka

kubectl port-forward controlcenter-0 9021:9021

### Argument local testing

--drivers driver-rabbitmq/new_rabbitmq.yaml --workers http://127.0.0.1:80,http://127.0.0.1:81 workloads/1-topic-1-partition-1kb.yaml

--drivers driver-rabbitmq/new_rabbitmq.yaml --workers http://localhost:8080,http://localhost:8080 workloads/1-topic-1-partition-1kb.yaml

### Add workload manually
Navigate to benchmark-driver </br>
kubectl exec -ti benchmark-driver -- //bin/bash

Copy file and rename it </br>
cp 0K-rate-1KB-size-1-topic-1-partitions-1p-1c.yaml 0K-rate-1KB-size-1-topic-1-partitions-3p-3c.yaml

Change number of consumer per subscription </br>
sed -i 's/consumerPerSubscription: 1/consumerPerSubscription: 3/g' 0K-rate-1KB-size-1-topic-1-partitions-3p-3c.yaml

-------------------------------------------------------
Change number of producers per topic </br>
sed -i 's/producersPerTopic: 1/producersPerTopic: 3/g' 0K-rate-1KB-size-1-topic-1-partitions-3p-3c.yaml

--------------------------------------------------------
Change producer rate from max till 1000 </br>
sed -i 's/producerRate: 0/producerRate: 1000/g' 1K-rate-1KB-size-1-topic-1-partitions-3p-3c.yaml

# Azure Kubernetes Services

----------------------------------------------

### Start Cluster

az aks start --name degree_v1 --resource-group degree-test-group </br>
az aks show --name degree_v1 --resource-group degree-test-group

### Stop Cluster

az aks stop --name degree_v1 --resource-group degree-test-group </br>
az aks show --name degree_v1 --resource-group degree-test-group

### Scale Node pool manually

az aks nodepool scale --resource-group degree-test-group --cluster-name degree_v1 --name agentpool --node-count 3 --no-wait </br>
az aks scale --resource-group degree-test-group --name myAKSCluster --node-count 1 --nodepool-name agentpool

### List status of node pool

az aks nodepool list -g degree-test-group --cluster-name degree_v1

# Azure Container Register

----------------------------------------------

### Login Azure

az login

### Login Azure Container Registry

az acr login --name degree

### Docker login ACR

docker login Degree.azurecr.io </br>
Fill in username "Degree" and password from ACR Access Key </br>

### Build Maven Project

mvn clean verify -DskipTests

### Export Tarball

export BENCHMARK_TARBALL=package/target/openmessaging-benchmark-0.0.1-SNAPSHOT-bin.tar.gz

### Build Docker image

docker build --build-arg BENCHMARK_TARBALL . -f docker/Dockerfile

### Tag docker image

docker tag <IMAGE_ID> Degree.azurecr.io/benchmark:main

### Push image to ACR

docker push Degree.azurecr.io/benchmark:main

# Helm

----------------------------------------------

### Login to Helm repo on ACR

ACR_NAME=Degree </br>
USER_NAME="00000000-0000-0000-0000-000000000000" </br>
PASSWORD=$(az acr login --name $ACR_NAME --expose-token --output tsv --query accessToken)

helm registry login $ACR_NAME.azurecr.io --username $USER_NAME --password $PASSWORD

### Create and Push Helm package to ACR

helm package ./deployment/kubernetes/helm/benchmark/ </br>

helm push openmessaging-benchmark-0.0.1.tgz oci://$ACR_NAME.azurecr.io/helm

### Install helm chart from repo

helm install benchmark oci://$ACR_NAME.azurecr.io/helm/openmessaging-benchmark --version 0.0.1

# RabbitMQ

----------------------------------------------

### Set namespace

kubectl config set-context --current --namespace default

### Install cluster operator and broker

helm install my-release bitnami/rabbitmq-cluster-operator

kubectl apply -f ./deployment/kubernetes/rabbitmq/definition.yaml

### Uninstall broker

kubectl delete -f ./deployment/kubernetes/rabbitmq/definition.yaml

### Pod Authentication to Rabbitmq

All username and password needs to be added to new_rabbitmq.yaml file to make access possible for worker pods</br>

password="$(kubectl get secret definition-default-user -o jsonpath='{.data.password}' | base64 --decode)" </br>
username="$(kubectl get secret definition-default-user -o jsonpath='{.data.username}' | base64 --decode)" </br>
service="$(kubectl get service definition -o jsonpath='{.spec.clusterIP}')" </br>

echo "username: $username"

### Port-forward management tool rabbitmq

kubectl port-forward "service/definition" 15672

The following is for logging in to the management tool  </br>
username: guest </br>
password: guest </br>

Default username is changed if new definition is installed. New credentials will have to be added to file new_rabbitmq.yaml in driver-rabbitmq
but only if the definition does not have predefined username and password

# Kafka

----------------------------------------------------

### Create a namespace

kubectl create namespace kafka

### Set namespace

kubectl config set-context --current --namespace kafka

### Install Strimzi Operator

kubectl create namespace kafka </br>
kubectl create -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka

kubectl logs deployment/strimzi-cluster-operator -n kafka -f

bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning

### Delete Strimzi Operator

Deletes the all the resources connected to Kafka, including bridge, zookeeper and brokers. </br>

kubectl delete -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka

### Create and Delete Kafka Ephemeral cluster

kubectl apply -f ./deployment/kubernetes/kafka/kafka-ephemeral.yaml -n kafka </br>
kubectl delete -f ./deployment/kubernetes/kafka/kafka-ephemeral.yaml -n kafka

### Create and Delete Modified Kafka Ephemeral cluster

This file is for testing to reduce effects of storage saturation </br>

kubectl apply -f ./deployment/kubernetes/kafka/kafka-ephemeral-modified.yaml -n kafka </br>
kubectl delete -f ./deployment/kubernetes/kafka/kafka-ephemeral-modified.yaml -n kafka

### Install bridge

kubectl apply -f ./deployment/kubernetes/kafka/kafka-bridge.yaml

### Watch Topics in Kafka

kubectl exec -ti my-cluster-kafka-0 -- //bin/bash
bin/kafka-topics.sh --bootstrap-server my-cluster-kafka-bootstrap:9092 --list

# Manual Tests

----------------------------------------------------

### Prerequisite: Set up kubernetes context

Change to the namespace depending on broker to be tested </br>
kubectl config set-context --current --namespace default
kubectl config set-context --current --namespace kafka

### 1. RabbitMQ set up (option 1)

Make sure operators and broker instance are installed, then install helm chart and forward to management tool
helm install benchmark oci://$ACR_NAME.azurecr.io/helm/openmessaging-benchmark --version 0.0.1

### 1. Install set up for Kafka tests (option 2)

1. Create the Cluster Operators, wait till running
   kubectl create -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka

2. Create Kafka brokers and Zookeper, wait till running
   kubectl apply -f ./deployment/kubernetes/kafka/kafka-ephemeral-modified.yaml

3. Create Htlm bridge for communication between pods, wait till running
   kubectl apply -f ./deployment/kubernetes/kafka/kafka-bridge.yaml

4. Create pods for openmessaging benchmark, wait till running
   helm install benchmark oci://$ACR_NAME.azurecr.io/helm/openmessaging-benchmark --version 1.0.0

### 2. Run test for RabbitMQ (option 1)

1. Access benchmark driver CLI
   kubectl exec -ti benchmark-driver -- //bin/bash

2. Check directory and adjust command before running tests. See tests.txt </br>
   bin/benchmark --drivers driver-rabbitmq/new_rabbitmq.yaml --workers $WORKERS workloads/tests/Throughput_tests/0K-rate-100B-size-1-topic-1-partitions-4p-4c.yaml </br>
   bin/benchmark --drivers driver-rabbitmq/new_rabbitmq.yaml --workers $WORKERS workloads/tests/1-topic-1-partitions-1kb-4p-4c-50k.yaml

### 2. Run Kafka driver (option 2)

1. Access benchmark driver CLI
   kubectl exec -ti benchmark-driver -- //bin/bash
2. Check directory and adjust command before running tests. See tests.txt </br>
   bin/benchmark --drivers driver-kafka/kafka-exactly-once-rep3.yaml --workers $WORKERS workloads/Kafka/1-topic-1-partition-1kb.yaml </br>
   bin/benchmark --drivers driver-kafka/kafka-exactly-once-rep3.yaml --workers $WORKERS workloads/Kafka/1-topic-100-partitions-1kb-4p-4c-200k.yaml

### 3. Copy the result from pod to current directory

kubectl cp default/benchmark-driver:<sourcefile> <targetfile> </br>
kubectl cp kafka/benchmark-driver:<sourcefile> <targetfile>

Example:
kubectl cp default/benchmark-driver:1-topic-1-partition-1kb-RabbitMQ-2024-02-05-15-54-53.json 1-topic-1-partition-1kb-RabbitMQ-2024-02-05-15-54-53.json

### 4. Reset RabbitMQ (option 1)

Exchange and queues needs to be deleted from the management tool before running new test to clean broker

helm uninstall benchmark

### 4. Uninstall set up for Kafka tests (option 2)

kubectl delete -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka

helm uninstall benchmark

