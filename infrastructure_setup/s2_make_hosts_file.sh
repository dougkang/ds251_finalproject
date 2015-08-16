#!/bin/bash

while getopts s: opt
do
    case $opt in 
        s) MAGIC_STR=${OPTARG};;
    esac
done

if [ -z "${MAGIC_STR}" ]
then
    echo "MAGIC_STR cannot be empty"
    exit 1
fi

echo "127.0.0.1   localhost.localdomain localhost" > hosts
slcli vs list | grep ${MAGIC_STR} | awk -F ' ' '{print $4,$2}' >> hosts
slcli vs list | grep ${MAGIC_STR} | awk -F ' ' '{print $3}' > external_ips

CSSH="cssh "
for h in $(cat external_ips)
do
    scp ~/.ssh/id_rsa root@${h}:/root/.ssh
    scp ~/.ssh/id_rsa.pub root@${h}:/root/.ssh
    scp ./hosts root@${h}:/etc/hosts
    CSSH="$CSSH root@$h "
done

echo "Please use the following command to cssh to each machine and make sure ssh inter hosts are really passwordless before continuing..."
echo "$CSSH"
