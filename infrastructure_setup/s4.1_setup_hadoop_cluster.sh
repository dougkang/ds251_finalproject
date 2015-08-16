#!/bin/bash

#DISK=$(cat /proc/partitions | sort -k3 | awk -F ' ' '{print $4}' | grep xvd | head -1)

salt-ssh '*' 'mkdir -m 777 /data'
salt-ssh '*' 'mkfs.ext4 /dev/xvdc'
salt-ssh '*' "echo '/dev/xdc    /data   ext4    defaults,noatime    0 0' >> /ets/fstab"
salt-ssh '*' "mount /data"
salt-ssh '*' "apt-get install -y default-jre default-jdk"
salt-ssh '*' "cd /usr/local; wget http://apache.claz.org/hadoop/core/hadoop-2.6.0/hadoop-2.6.0.tar.gz; tar xzf hadoop-2.6.0.tar.gz; mv hadoop-2.6.0 hadoop"
salt-ssh '*' "adduser hadoop"
salt-ssh '*' "chown -R hadoop.hadoop /data"
salt-ssh '*' "chown -R hadoop.hadoop /usr/local/hadoop"
salt-ssh '*' "cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys"
salt-ssh '*' "mv ~hadoop/.ssh{,-old}"
salt-ssh '*' "cp -a ~/.ssh ~hadoop/.ssh"
salt-ssh '*' "chown -R hadoop ~hadoop/.ssh"
echo "ssh to all hosts and check user hadoop can ssh passwordless"
CSSH="cssh "
for h in $(cat external_ips)
do
    CSSH="$CSSH root@$h "
done

echo "$CSSH"
