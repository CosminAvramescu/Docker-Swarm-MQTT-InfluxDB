#! /bin/bash

docker swarm init
docker build -t adapter .

# docker stack deploy -c stack.yml sprc3

# python3 iot_simulator.py

# docker stack rm sprc3
