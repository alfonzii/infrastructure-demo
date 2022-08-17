#!/bin/bash

# Run this script ONLY from root (sudo -s)

# Make volume mount on reboot
echo 'localhost:/gluster_vol0 /mnt/ifr-demo_vol glusterfs defaults,_netdev,backupvolfile-server=localhost 0 0' >> /etc/fstab

# Mount volume
mount.glusterfs localhost:/gluster_vol0 /mnt/ifr-demo_vol

chown -R root:docker /mnt/ifr-demo_vol

# Add all permissions to /mnt/ifr-demo_vol directory
# chmod a+rwx /mnt/ifr-demo_vol
# chmod a+rwx /mnt/ifr-demo_vol/logs
# chmod a+rwx /mnt/ifr-demo_vol/shelve



# Check with df -h if you are mounted to GlusterFS volume
