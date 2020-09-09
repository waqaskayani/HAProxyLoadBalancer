# **Table Of Contents**

1. Introduction
2. Flask Application
3. Setting up HAProxy
4. Running script and testing

## **1. Introduction**

This repo is for a demo app to show how open source tools can be used to auto-scale and load-balance a web application. The web application is created using Flask and HAProxy is used to balance the load by spreading requests across multiple servers.

## **2. Flask Application**

We create a simple Flask application that shows the host name. Code for application is in app.py file is in `image` directory. The server is started using `Flask.run()` method in main block, and `debug=True` is passed to enable debugger and reloader. The created Flask application listens to IP `0.0.0.0` and port `5000` of host machine.

### **Dockerfile**
The dockerfile, located in `image` directory, is used to create a docker image, that will be used to run containers. The following can be run to create an image (you may choose image name of choice):
```
docker build --tag <docker-image-name> .
```


## **3. Setting up HAProxy**

Fetch package index and install/update haproxy package:
```
sudo apt update -y && sudo apt install haproxy
```
Make a backup of your config:
```
sudo cp /etc/haproxy/haproxy.cfg /etc/haproxy/haproxy.cfg.bak
```
Check status of HAProxy service:
```
sudo systemctl status haproxy.service
```
Copy the haproxy.cfg from repo to /etc/haproxy/haproxy.cfg and restart service:
```
sudo cp haproxy.cfg /etc/haproxy/haproxy.cfg
sudo systemctl restart haproxy.service
sudo systemctl status haproxy.service
```
Test the working of HAProxy server by entering in web-browser:
```
0.0.0.0:5050/haproxy?stats
```
This configuration will make HAProxy service listen at frontend socket 0.0.0.0:5050 for requests and forwards them at the backend servers that will be created when the script runs.


## **4. Running script and testing**

First, we need to install stress tool
```
sudo apt-get install stress
```
Try and make sure it is working. Press ctrl+C to exit the stress afterwards:
```
sudo stress --cpu 2  # this code will stress 2 cores of CPU
```
**Note:** Make sure to replace 2 in the above command accordingly. If you input more than your available CPU cores (e.g. 20), it will make the system unstable.

Now, before you run the main "task.py" script, edit `add_container_cfg.sh` and replace the `<docker-image-name>` with the name of your image created. This is the image that will be used to start all containers when the script will execute.
```
sudo docker images  # to see docker image name
```
Execute task.py:
```
python3 task.py
```
**Note:** When stress on CPU is increased using stress tool, since the average CPU usage percentage fluctuates at first, before being stable after a couple of seconds, and the containers are created/removed based on that. To make the entire functioning smooth, the script requires an input from user after each step, so the user can proceed by pressing enter key, once the CPU usage is stable.

**Testing resuls:**
To test HAProxy load balancing, you have to enter frontend ip and port, and refresh the page to see hostnames of all containers started. You can alternately visit HAproxy statistics report, e.g. with repository's haproxy.cfg, frontend ip is 0.0.0.0 and port is 5050. You will visit:
```
0.0.0.0:5050/haproxy?stats
```


## **5. Troubleshooting**

In any case any wrong changes are made in HAproxy configuration file (located in /etc/haproxy/haproxy.cfg) or any container(s) is/are created using given script by mistake, you can run `reset.sh` script to restore the default config file back and stop/remove any containers.
```
bash ./reset.sh
```
