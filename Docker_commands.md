# Docker Commands

## Plain Docker Commands

List images: <br/>
docker image ls

Remove image: <br/>
docker image rm <Reponame_to_remove>

Build image from docker file in current directory: <br/>
docker build gnormelli/<name_repo>:<tag_name> .

gnormelli/benchmark:v2

Run containter: <br/>
docker run <tag_name>
docke
To push a new tag to this repository: <br/>
docker push gnormelli/test_repo:<tag_name>

Retag an image: <br/>
* docker tag <current_name> gnormelli/<new_name>:<version_tag> <br/>

### Generic docker commands

* -d: run docker in detached mode
* -i: Keep STDIN open even if not attached
* -t: Allocate a pseudo-TTY
* -it: The -it instructs Docker to allocate a pseudo-TTY connected
  to the container's stdin; creating an interactive bash shell in the container.
* docker exec: Execute a command in a running container
* -p <machine_port>:<container_port> : set up port from inside container to outside machine

Example: docker exec -it <container_name_or-id> bash
Example: docker exec -it  --user root <container_name_or-id> bash

### Docker-compose for kafka

docker-compose -f  docker-compose.yaml up -d

### Azure Image Registry

* Retag for Azure:
* docker tag <current_name> myregistry.azurecr.io/<new_name>:<version_tag>

Log in to registry:
* az login
* az acr login --name degree
* docker login degree.azurecr.io <br/>
username and password found under Access keys on Azure Containter Registry

Push image to Azure Image Registry
* docker push degree.azurecr.io/<image_name>:<image_tag>

https://learn.microsoft.com/en-us/azure/container-registry/container-registry-get-started-docker-cli?tabs=azure-cli

Create and run container instance
* az container create --resource-group Resource_group_test --name degree-container-instance --image degree.azurecr.io/my_docker_image:v1 --registry-login-server degree.azurecr.io --registry-username degree --registry-password CDTaPUL7gUjJMUPGIkuguW4I8r38PMZHpNuxfJ18mD+ACRDZD0PK --dns-name-label degree-container-dns --ports 80
* az container show --resource-group Resource_group_test --name degree-container-instance --query "{FQDN:ipAddress.fqdn,ProvisioningState:provisioningState}" --out table

Open bash shell from azure
* az container exec --resource-group Resource_group_test --name degree-container-instance --exec-command "/bin/bash"

## Jmeter Specific Commands with Docker

### Command used for running example tests on localhost

docker run jmeter -n -t bin/examples/CSVSample.jmx -l ./bin/examples/Run1.jtl

### Get tests result by copying from image

mkdir jmeter-results <br />

docker cp <image_containerID>: <directory_in_image . > <br />

Example: <br /> docker cp e4593a83064d:/opt/apache-jmeter-5.3/bin/examples <br />

### Alternative Bind Mount for Test Tesults

Example: <br /> docker run --mount type=bind, source="/mnt/c/Tools/apache-jmeter-5.4.1/bin/".target="/opt/apache-jmeter5.3/bin/example.jmx -l bin/example-run1.jtl

### Generic Jmeter Command Line Commands

n: CLI mode (also called non-GUI mode in JMeter) <br />
l: Result file directory <br />
t: JMeter scripts file directory <br />
H: The proxy address <br />
P: The proxy port <br />
Example: <br />
jmeter -n -l results.csv -t MyScript.jmx -JNumberOfUnits=100 -Jrampup=50 -JNumberOfIterations=1000 -H myProxy.xom -P 9999

        jmeter -n -t -l 

### Grafana

docker run -d --name=grafana -p 4000:3000 grafana/grafana

### InfluxDB

docker run -d --name=influxdb -p 9002:8086 influxdb
