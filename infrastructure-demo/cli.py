import subprocess

print("Hello, welcome to high availability docker infrastructure demo! Please run in sudo mode to avoid permission problems with docker.\n")
print("\
Commands:\n\
pullimages - pulls images required for the demo from docker hub\n\
deploy - deploys the application into docker swarm (can be run without pullimages - \"deploy\" downloads images if not present on its own)\n\
scale <SERVICE> <NUMBER-OF-TASKS> - scales services in this demo by given number of tasks. There are 4 services which can be used as arguments: \"db\", \"web\", \"logger\" and \"visualizer\"\n\
update - updates application if there is any newer image of some service on the hub\n\
info - provides info about running demo\n\
logs - prints out logs which were already written by logger\n\
quit - quits the demo and CLI application\n\
\n\
To exit CLI but not quit demo, just hit Ctrl + D\
")

def pullimages():
    subprocess.run(["docker", "pull", "alfonzi/web-app:latest"])
    subprocess.run(["docker", "pull", "alfonzi/db-app:latest"])
    subprocess.run(["docker", "pull", "alfonzi/logger-app:latest"])
    subprocess.run(["docker", "pull", "dockersamples/visualizer:stable"])
    
def deploy():
    subprocess.run(["docker", "stack", "deploy", "--compose-file", "docker-compose-shared.yml", "ifr-demo"])
    
def update():
    pullimages()
    deploy()
    
def scale(service: str, num: int):
    subprocess.run(["docker", "service", "scale", "ifr-demo_" + service + "=" + str(num)])
    
def info():
    subprocess.run(["docker", "stack", "services", "ifr-demo"])
    print()
    subprocess.run(["docker", "stack", "ps", "ifr-demo"])
    print("\nNodes info:")
    subprocess.run(["docker", "node", "ls"])
    
def logs():
    subprocess.run(["cat", "/mnt/ifr-demo_vol/logs/ifr-demo.log"])
    
def quit():
    subprocess.run(["docker", "stack", "rm", "ifr-demo"])

while True:
    command = input("\nEnter command: ")
    
    if (command == "pullimages"):
        pullimages()
        
    elif (command == "deploy"):
        deploy()
        
    elif (command == "update"):
        update()
        
    elif (command == "info"):
        info()
        
    elif (command == "logs"):
        logs()
        
    elif (command == "quit"):
        quit()
        break;
        
    else:
        commList = command.split()
        if len(commList) != 3:
            print("Invalid command.")
            continue
        else:
            if commList[0] != "scale":
                print("Invalid command.")
                continue
            else:
                try:
                    num = int(commList[2])
                except ValueError:
                    print("Expected second argument is not a number.")
                    continue
                service = commList[1]
                if service == "web" or service == "db" or service == "logger" or service == "visualizer":
                    scale(service, num)
                else:
                    print("Invalid service to scale. Please use \"db\", \"web\", \"logger\" or \"visualizer\" as service argument")
                    continue
        #print("Invalid command")
