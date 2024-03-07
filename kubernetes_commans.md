$ kubectl get nodes: get node

$ kubectl get po --all-namespaces: get all the pods within namespace

$ kubectl get all: get all pods and namespaces, cluster-ip, ports etc

$ kubectl get pods -o wide

### Minikube start

minikube start -p kafka --cpus=4 --memory=4096
minikube start -p kafka --cpus=4 --memory=6144

Switch by:
minikube profile kafka

### Creat secrete

kubectl create secret generic regcred --from-file=.dockerconfigjson="C:\Users\Gustav Normelli\.docker\config.json" --type=kubernetes.io/dockerconfigjson

password="dckr_pat_HeWjwWNwUZR0Uc43Xv0e1LAfmZw"
username="gnormelli"

echo "username: $username"
echo "password: $password"

kubectl create secret docker-registry regcred --docker-server="https://index.docker.io/v1/" --docker-username="$username" --docker-password="$password" --docker-email="gustav.normelli@gmail.com"

# Misilanious commands minikube

kubectl config get-contexts

kubectl cp driver-rabbitmq/new_rabbitmq.yaml benchmark-driver:/benchmark/driver-rabbitmq

### Access Benchmark driver CLI & run benchmark

kubectl exec -ti benchmark-driver -- //bin/bash

bin/benchmark --drivers driver-rabbitmq/new_rabbitmq.yaml --workers $WORKERS workloads/1-topic-1-partitions-1kb.yaml
bin/benchmark --drivers driver-rabbitmq/new_rabbitmq.yaml --workers $WORKERS workloads/1-topic-100-partitions-1kb-4p-4c-200k.yaml

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

# RabbitMQ

### Install cluster operator and broker

helm install my-release bitnami/rabbitmq-cluster-operator

kubectl apply -f ./deployment/kubernetes/rabbitmq/definition.yaml

### Authentication Rabbitmq

password="$(kubectl get secret definition-default-user -o jsonpath='{.data.password}' | base64 --decode)"
username="$(kubectl get secret definition-default-user -o jsonpath='{.data.username}' | base64 --decode)"
service="$(kubectl get service definition -o jsonpath='{.spec.clusterIP}')"

echo "username: $username"

### Port-forward management tool rabbitmq

kubectl port-forward "service/definition" 15672

# Azure

----------------------------------------------

### Set context

kubectl config use-context degree_v1

### Push Helm package to ACR

helm package .
ACR_NAME=Degree
USER_NAME="00000000-0000-0000-0000-000000000000"
PASSWORD=$(az acr login --name $ACR_NAME --expose-token --output tsv --query accessToken)

helm registry login $ACR_NAME.azurecr.io --username $USER_NAME --password $PASSWORD

helm push openmessaging-benchmark-0.0.1.tgz oci://$ACR_NAME.azurecr.io/helm

### Install helm chart from repo

helm install benchmark oci://$ACR_NAME.azurecr.io/helm/openmessaging-benchmark --version 0.0.1

### Push Image to ACR

az acr token create --name DegreeToken --registry degree --repository gnormelli/benchmark content/write content/read --output json

### Copy the result from pod to current directory

kubectl cp default/benchmark-driver:<sourcefile> <targetfile>

Example:
kubectl cp default/benchmark-driver:1-topic-1-partition-1kb-RabbitMQ-2024-02-05-15-54-53.json 1-topic-1-partition-1kb-RabbitMQ-2024-02-05-15-54-53.json

### Generate Charts from result

python bin/create_charts.py <chartfile>

# Kafka

----------------------------------------------------

### Create a namespace

kubectl create namespace <namespace>

### Set namespace to default

kubectl config set-context --current --namespace <namespace>

### Run Kafka driver

kubectl exec -ti benchmark-driver -- //bin/bash

bin/benchmark --drivers driver-kafka/kafka-exactly-once-rep3.yaml --workers $WORKERS workloads/1-topic-1-partition-1kb.yaml

### Create and Delete kafka cluster

kubectl apply -f ./deployment/kubernetes/kafka/kafka-persistent.yaml -n kafka
kubectl delete -f ./deployment/kubernetes/kafka/kafka-persistent.yaml -n kafka

### Watch Topics in Kafka

kubectl exec -ti my-cluster-kafka-0 -- //bin/bash
bin/kafka-topics.sh --bootstrap-server my-cluster-kafka-bootstrap:9092 --list

### Install bridge

kubectl apply -f ./deployment/kubernetes/kafka/kafka-bridge.yaml

### Install Strimzi Operator

kubectl create namespace kafka
kubectl create -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka

kubectl logs deployment/strimzi-cluster-operator -n kafka -f

kubectl apply -f https://strimzi.io/examples/latest/kafka/kafka-persistent-single.yaml -n kafka

bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning
