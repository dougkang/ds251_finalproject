#!/bin/bash

cat <<_EOF
This step will start up the hadoop by the following step

For master node, start everything.
/usr/local/hadoop/sbin/hadoop-daemon.sh --config /usr/local/hadoop/etc/hadoop --script hdfs start namenode
/usr/local/hadoop/sbin/yarn-daemon.sh --config /usr/local/hadoop/etc/hadoop/ start resourcemanager
/usr/local/hadoop/sbin/yarn-daemon.sh start proxyserver --config /usr/local/hadoop/etc/hadoop/
/usr/local/hadoop/sbin/mr-jobhistory-daemon.sh start historyserver --config /usr/local/hadoop/etc/hadoop

For slave nodes, only start DataNode and NodeManager.
/usr/local/hadoop/sbin/yarn-daemon.sh --config /usr/local/hadoop/etc/hadoop/ start nodemanager
/usr/local/hadoop/sbin/hadoop-daemon.sh --config /usr/local/hadoop/etc/hadoop --script hdfs start datanode

To check your cluster, go to:
http://master-ip:50070/dfshealth.jsp
http://master-ip:8088/cluster
http://master-ip:19888/jobhistory (for Job History Server)
Log files are located under /usr/local/hadoop/logs
_EOF

ssh-salt 'master' "su - hadoop; /usr/local/hadoop/sbin/hadoop-daemon.sh --config /usr/local/hadoop/etc/hadoop --script hdfs start namenode"
ssh-salt 'master' "su - hadoop; /usr/local/hadoop/sbin/yarn-daemon.sh --config /usr/local/hadoop/etc/hadoop/ start resourcemanager"
ssh-salt 'master' "su - hadoop; /usr/local/hadoop/sbin/yarn-daemon.sh start proxyserver --config /usr/local/hadoop/etc/hadoop/"
ssh-salt 'master' "su - hadoop; /usr/local/hadoop/sbin/mr-jobhistory-daemon.sh start historyserver --config /usr/local/hadoop/etc/hadoop"

ssh-salt '*' "su - hadoop; /usr/local/hadoop/sbin/yarn-daemon.sh --config /usr/local/hadoop/etc/hadoop/ start nodemanager"
ssh-salt '*' "su - hadoop; /usr/local/hadoop/sbin/hadoop-daemon.sh --config /usr/local/hadoop/etc/hadoop --script hdfs start datanode"
