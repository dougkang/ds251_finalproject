#!/bin/bash

while getopts m: opt
do
    case $opt in 
        m)MASTER=${OPTARG};;
    esac
done

if [ -z "${MASTER}" ]
then
    echo "Please pass in MASTER hostname specified in /etc/hosts using -m"
    exit 1
fi

for h in $(cat external_ips)
do
    ssh root@${h} "apt-get -y install vim"
    ssh root@${h} "apt-get -y install python-software-properties"
    ssh root@${h} "apt-get -y install software-properties-common"
    ssh root@${h} "yes Y| sudo add-apt-repository ppa:saltstack/salt"
    ssh root@${h} "apt-get -y update"
    ssh root@${h} "apt-get -y install salt-master"
    ssh root@${h} "apt-get -y install salt-minion"
    ssh root@${h} "apt-get -y install salt-syndic"
    ssh root@${h} "apt-get -y install git"
    ssh root@${h} "apt-get -y install salt-ssh"
    ssh root@${h} "echo 'master:${MASTER}' >> /etc/salt/minion"
done

echo "Go to the master host and execute the following commands"
echo "salt-key -L"
echo "salt-key -A"
echo "run salt '*' test.ping to make sure things are fine, if needed run salt-minion restart -d on each minion node"

echo "Starting step 4, please run them on master node"
