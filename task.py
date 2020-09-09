from subprocess import call
from textwrap import dedent
from psutil import cpu_percent


class ContainerApp(object):

    def __init__(self, port_num = 1):
        self.port_num = port_num
        print(dedent("""
        Welcome to the application!

        This application will create simple flask application containers and will
        balance the load between them using HAProxy. 
        """))

    def add_container(self):
        call(['bash', './add_container_cfg.sh', f'{self.port_num}'])
        self.port_num += 1

    def remove_container(self):
        if self.port_num <= 1:
            print(f"The container app{self.port_num} does not exist. Please try again..\n")
        else:
            self.port_num -= 1
            call(['bash', './remove_container_cfg.sh', f'{self.port_num}'])

    def status_container(self):
        print("\n####### Docker Status #######")
        call("sudo docker ps".split())
        print("\n####### HAProxy Config #######")
        call("tail -10 /etc/haproxy/haproxy.cfg".split())
        print("\n")


if __name__ == "__main__":
    container_app = ContainerApp()
    curr_containers = 0

    while True:        
        # total_containers = int(input("Specify N number of containers: "))
        cpu_usage = cpu_percent(interval=1)
        total_containers = cpu_usage // 10
        print(f"Current CPU usage: {cpu_usage}")
        print(f"Number of containers to be created: {total_containers}")
        input("Press any key to start")

        if curr_containers < total_containers:
            print("\nContainers will be created..")
            while curr_containers < total_containers:
                container_app.add_container()
                curr_containers += 1
            print("\nContainers created. Current status:")
            container_app.status_container()
            input("Press any key to continue...\n")

        elif curr_containers > total_containers:
            print("\nContainers will be removed..")
            while curr_containers > total_containers:
                container_app.remove_container()
                curr_containers -= 1
            print("\nContainers removed. Current status:")
            container_app.status_container()
            input("Press any key to continue...\n")

        else:
            print("\nNo further changes in CPU usage detected. ")
            input("Press any key to detect again...\n")
