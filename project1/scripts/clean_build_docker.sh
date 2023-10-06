#!/bin/bash

sudo docker image rm $(sudo docker image ls --format '{{.Repository}} {{.ID}}' | grep 'mengtianjian' | awk '{print $2}')

cd dockerfiles

sudo docker build . -f base.dockerfile -t mengtianjian/dist_sys_project1:base --network=host
sudo docker push mengtianjian/dist_sys_project1:base

sudo docker build . -f client.dockerfile -t mengtianjian/dist_sys_project1:client --network=host
sudo docker push mengtianjian/dist_sys_project1:client

sudo docker build . -f frontend.dockerfile -t mengtianjian/dist_sys_project1:frontend --network=host
sudo docker push mengtianjian/dist_sys_project1:frontend

sudo docker build . -f server.dockerfile -t mengtianjian/dist_sys_project1:server --network=host
sudo docker push mengtianjian/dist_sys_project1:server

cd ..
