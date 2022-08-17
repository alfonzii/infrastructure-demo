#!/bin/bash

# install the necessary dependencies
sudo apt install software-properties-common -y

# add the necessary repository 
sudo add-apt-repository ppa:gluster/glusterfs-10

sudo apt update
sudo apt install glusterfs-server -y

# start and enable GlusterFS
sudo systemctl start glusterd
sudo systemctl enable glusterd


# generate SSH keygen
ssh-keygen -t rsa

# create dir used for Gluster volume
sudo mkdir -p /gluster/ifr-demo_vol

# create volume dir for infrastrucutre demo
sudo mkdir -p /mnt/ifr-demo_vol
