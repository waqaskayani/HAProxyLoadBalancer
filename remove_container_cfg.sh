#!/bin/bash

sudo docker container inspect app$1 &> /dev/null
if [ "$?" -eq 0 ]; then

    # Remove last server line from HAproxy configuration
    sed -i '$d' haproxy.cfg
    sudo cp haproxy.cfg /etc/haproxy/haproxy.cfg
    sudo systemctl restart haproxy.service
    
    # Stop and remove the container
    sudo docker stop app$1
    sudo docker rm app$1

else
    echo -ne "The container \"app$1\" does not exist. Try again..\n"
fi
