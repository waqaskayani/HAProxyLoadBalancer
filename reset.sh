#!/bin/bash

sudo cp haproxy.cfg.bak haproxy.cfg
sudo cp haproxy.cfg /etc/haproxy/haproxy.cfg

for i in $(sudo docker ps | grep -i "app." | awk '{print $1}') 
do
    sudo docker stop $i
    sudo docker rm $i
done
