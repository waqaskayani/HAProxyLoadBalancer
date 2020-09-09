#!/bin/bash

# Add backend server to HAproxy configuration and copy to default dir
echo -ne "\tserver srv$1 0.0.0.0:505$1\n" >> haproxy.cfg
sudo cp haproxy.cfg /etc/haproxy/haproxy.cfg
sudo systemctl restart haproxy.service

# Start container in detached mode
sudo docker run -d --name app$1 -p 505$1:5000 <docker-image-name>
