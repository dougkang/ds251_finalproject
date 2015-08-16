#!/bin/bash

while getopts s: opt
do
    case $opt in 
        s) MAGIC_STR=${OPTARG};;
    esac
done

echo "127.0.0.1   localhost.localdomain localhost" > hosts
slcli vs list | grep ${MAGIC_STR} | awk -F ' ' '{print $4,$2}' >> hosts
slcli vs list | grep ${MAGIC_STR} | awk -F ' ' '{print $3}' > external_ips

for h in $(cat external_ips)
do
    scp ~/.ssh/id_rsa root@${h}:/root/.ssh
    scp ~/.ssh/id_rsa.pub root@${h}:/root/.ssh
done


