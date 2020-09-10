#!/bin/bash

sudo cp haproxy.cfg.bak haproxy.cfg
sudo cp haproxy.cfg /etc/haproxy/haproxy.cfg
sudo systemctl restart haproxy.service

echo -ne "HAProxy service successfully reset to default configuration...\n"

for i in $(sudo docker ps | grep -i "app." | awk '{print $1}') 
do
    sudo docker stop $i
    sudo docker rm $i
done

echo -ne "All Docker containers created using the script successfully stopped and removed..\n"
