# infrastructure-demo

## Intro
Ever wondered how **high availability (HA)** looks like in practice? Wanted to get your hands dirty, but examples on internet look complicated and difficult for you to start? This "package" provides you with simple setup to make HA environment ready for you on your own cluster of 3 VMs and application (with CLI) on this cluster that does all the dirty work for you, so you can just start experimenting with high availability right away and see for yourself.

## Overview
- Simple application demonstrating how using containerization can lead to better scalability and robustness of app
- HA environment cluster consisting of 3 VMs
- Divided on two parts:
  1. Setup of HA environment in this cluster
  2. Running infrastructure demo app in such environment for demonstration
  
- Consists of 4 services (web, database, logger, visualizator) and CLI app for easy orchestration
- Technologies used:
  - Containerization - Docker
  - Orchestration - Docker Swarm
  - HA distributed storage - GlusterFS
  - Programming language - Python
  - Webserver - Python Flask  

## Setup
To be able to use application, we first need to setup environment for it. In this section we will provide instructions on how to correctly setup cluster of 3 VMs to properly run our infrastructure demo in it. You **MUST FOLLOW** these instructions **EXACTLY** as they are. It's tested and it will provide you with needed environment. Should you run commands or follow instructions in different order as they are written here, there is no warranty it will create needed environment for you! 

### VM install and docker swarm setup
1. Download [Ubuntu 22.04.1 LTS 64-bit](https://ubuntu.com/download/desktop)
2. Install it on 3 VMs -> minimal install -> for machine names (hostnames) I used *ubuntu1-vm*, *ubuntu2-vm*, *ubuntu3-vm* but you can use anything you'd like -> everything accept and continue (I used VMware Workstation 15 software for virtual machines, but I suppose any other VM software should be good as well)
3. `python3` should be installed by default (3.10.4), but should it from any reason not be, then install it.
4. Copy `demo-init` folder (or all scripts from it) to all VMs - it contains all necessary installation and initialization scripts
5. Run `bash docker-install.sh` on all machines from `demo-init` folder. This will install docker (and it's dependencies) and adds user into docker group so we won't be needing to run docker always with `sudo`.
6. reboot (to make this permission with `sudo` and docker group work)
7. Follow `add-hosts.txt` file to add hosts into VMs
8. On **JUST ONE of VMs** we will initialize docker swarm by running `docker swarm init --advertise-addr MASTER_IP`, where MASTER_IP is IP of given VM where are we running docker swarm init (IP of this VM from these 3 IPs which we gave into `/etc/hosts`). Let's call this machine MASTER.
9. Ignore the output of this command on MASTER machine. Subsequently, run on it command `docker swarm join-token manager`. It will return something like `docker swarm join --token SWMTKN-1-09c0p3304ookcnibhg3lp5ovkjnylmxwjac9j5puvsj2wjzhn1-2vw4t2474ww1mbq4xzqpg0cru 192.168.1.67:2377`
10. Run this command on other 2 VMs and they should connect to swarm as managers.

Right now, we should be in state, such that all 3 machines are connected to swarm as managers. We can check it by running `docker node ls` and should see all machines, from which one is leader and other 2 are reachable. If this is correct, then you are in desired state.
Just for info, we are connecting all machines to swarm as managers because of HA of nodes, so that if we simulate death of ONE node (any of them), whole infrastructure will be further working.

This setup was created mostly by compilation of these three websites ([1](https://thenewstack.io/tutorial-create-a-docker-swarm-with-persistent-storage-using-glusterfs/), [2](https://docs.docker.com/engine/install/ubuntu/), [3](https://docs.docker.com/engine/install/linux-postinstall/))

### GlusterFS install and initialization
(all nodes must be up and running during Gluster cluster initialization)
1. On every machine we run `bash glusterfs-install.sh` (located in `demo-init`) - it will install GlusterFS for us and creates required directories
2. We switch into root `sudo -s` on all machines
3. On **one and just one** machine (eg. MASTER) run `bash glusterfs-master-init.sh` This file needs to be properly rewritten on specific places, such that hostnames are same as we put them in `/etc/hosts`. Running this master init script will connect other VMs into gluster network, creates gluster volume, runs it and mount it.
4. Now, **AFTER** running `bash glusterfs-master-init.sh` on MASTER, we will run `bash glusterfs-slave-init.sh` on remaining 2 VMs. It'll initialize and mount gluster.
5. You can exit from root with `exit`

At this very moment, you should have whole environment ready for you to run **_infrastructure-demo_** program. To check, if you are properly connected to gluster and got the volume mounted, run `df -h` and see for yourself (you should be able to see one volume with gluster keyword in it).

Last but not least, it you quit 2 or 3 VMs (generally speaking more than 50% of machines), then, at reboot, it's needed for you to mount again gluster volume (when there are already more then 50% of machines up) with command `sudo mount.glusterfs localhost:/gluster_vol0 /mnt/ifr-demo_vol`
