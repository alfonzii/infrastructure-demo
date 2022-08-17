#!/bin/bash

# Run this script ONLY from root (sudo -s)

# Ping other VMs to connect them to master
# Copy and change hostname arguments to hostnames given in /etc/hosts for VMs which we did earlier
# gluster peer probe <NODE1-HOSTNAME>; gluster peer probe <NODE2-HOSTNAME>;
gluster peer probe ubuntu2-vm; gluster peer probe ubuntu3-vm;

# Check if all nodes are connected with `gluster pool list`

# Create volume
# Copy and change hostnames accordingly too
# sudo gluster volume create gluster_vol0 replica 3 <MASTER-HOSTNAME>:/gluster/ifr-demo_vol <NODE1-HOSTNAME>:/gluster/ifr-demo_vol <NODE2-HOSTNAME>:/gluster/ifr-demo_vol force
gluster volume create gluster_vol0 replica 3 ubuntu1-vm:/gluster/ifr-demo_vol ubuntu2-vm:/gluster/ifr-demo_vol ubuntu3-vm:/gluster/ifr-demo_vol force

# Start volume
gluster volume start gluster_vol0

# Make volume mount on reboot
echo 'localhost:/gluster_vol0 /mnt/ifr-demo_vol glusterfs defaults,_netdev,backupvolfile-server=localhost 0 0' >> /etc/fstab

# Mount volume
mount.glusterfs localhost:/gluster_vol0 /mnt/ifr-demo_vol

chown -R root:docker /mnt/ifr-demo_vol

# Add all permissions to /mnt/ifr-demo_vol directory
chmod a+rwx /mnt/ifr-demo_vol

# create dirs used by infrastructure demo
mkdir -p /mnt/ifr-demo_vol/logs
mkdir -p /mnt/ifr-demo_vol/shelve

# Add them all permissions
chmod a+rwx /mnt/ifr-demo_vol/logs
chmod a+rwx /mnt/ifr-demo_vol/shelve

# Check with df -h if you are mounted to GlusterFS volume
