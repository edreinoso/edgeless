#!/bin/bash

# Define the JSON payload
gp='{"topic":"lambda/greengrass/pinned"}'


# DOCKER W1
docker_100='{"topic":"thesis/docker","env":"docker","size":"100"}'
docker_300='{"topic":"thesis/docker","env":"docker","size":"300"}'
docker_500='{"topic":"thesis/docker","env":"docker","size":"500"}'
docker_700='{"topic":"thesis/docker","env":"docker","size":"700"}'
docker_1000='{"topic":"thesis/docker","env":"docker","size":"1000"}'
# W2
docker_5='{"topic":"thesis/docker","env":"docker","size":"5"}'
docker_10='{"topic":"thesis/docker","env":"docker","size":"10"}'
docker_20='{"topic":"thesis/docker","env":"docker","size":"20"}'
docker_25='{"topic":"thesis/docker","env":"docker","size":"25"}'
docker_50='{"topic":"thesis/docker","env":"docker","size":"50"}'

# GGP 
# W1
ggp_100='{"topic":"lambda/greengrass/pinned","env":"ggp","size":"100"}'
ggp_300='{"topic":"lambda/greengrass/pinned","env":"ggp","size":"300"}'
ggp_500='{"topic":"lambda/greengrass/pinned","env":"ggp","size":"500"}'
ggp_700='{"topic":"lambda/greengrass/pinned","env":"ggp","size":"700"}'
ggp_1000='{"topic":"lambda/greengrass/pinned","env":"ggp","size":"1000"}'
# W2
ggp_5='{"topic":"lambda/greengrass/pinned","env":"ggp","size":"5"}'
ggp_10='{"topic":"lambda/greengrass/pinned","env":"ggp","size":"10"}'
ggp_20='{"topic":"lambda/greengrass/pinned","env":"ggp","size":"20"}'
ggp_25='{"topic":"lambda/greengrass/pinned","env":"ggp","size":"25"}'
ggp_50='{"topic":"lambda/greengrass/pinned","env":"ggp","size":"50"}'

# NCP 
# W1
ncp_100='{"topic":"lambda/nocontainer/pinned","env":"ncp","size":"100"}'
ncp_300='{"topic":"lambda/nocontainer/pinned","env":"ncp","size":"300"}'
ncp_500='{"topic":"lambda/nocontainer/pinned","env":"ncp","size":"500"}'
ncp_700='{"topic":"lambda/nocontainer/pinned","env":"ncp","size":"700"}'
ncp_1000='{"topic":"lambda/nocontainer/pinned","env":"ncp","size":"1000"}'
# W2
ncp_5='{"topic":"lambda/nocontainer/pinned","env":"ncp","size":"5"}'
ncp_10='{"topic":"lambda/nocontainer/pinned","env":"ncp","size":"10"}'
ncp_20='{"topic":"lambda/nocontainer/pinned","env":"ncp","size":"20"}'
ncp_25='{"topic":"lambda/nocontainer/pinned","env":"ncp","size":"25"}'
ncp_50='{"topic":"lambda/nocontainer/pinned","env":"ncp","size":"50"}'

# NATIVE 
# W1
native_100='{"topic":"thesis/native","env":"native","size":"100"}'
native_300='{"topic":"thesis/native","env":"native","size":"300"}'
native_500='{"topic":"thesis/native","env":"native","size":"500"}'
native_700='{"topic":"thesis/native","env":"native","size":"700"}'
native_1000='{"topic":"thesis/native","env":"native","size":"1000"}'
# W2
native_5='{"topic":"thesis/native","env":"native","size":"5"}'
native_10='{"topic":"thesis/native","env":"native","size":"10"}'
native_20='{"topic":"thesis/native","env":"native","size":"20"}'
native_25='{"topic":"thesis/native","env":"native","size":"25"}'
native_50='{"topic":"thesis/native","env":"native","size":"50"}'

# Encode the payload as Base64
encoded_payload=$(echo -n "$ncp_300" | base64)

# Define the MQTT topic
start_exp_w1="thesis/start/w1"
start_exp_w2="thesis/start/w2"

aws iot-data publish \
    --topic "$start_exp_w1" \
    --payload "$encoded_payload"

echo -e "Send message to gateway component\n"
