#!/bin/bash

salt-ssh '*' "cat << _EOF >> /home/hadoop/.bashrc
export JAVA_HOME="/usr/lib/jvm/java-7-openjdk-amd64/jre"
export SPARK_HOME="/usr/local/spark"
export HADOOP_CONF_DIR="/usr/local/hadoop/etc/hadoop"
export PATH=$SPARK_HOME/bin:$PATH
export PYTHONPATH=$SPARK_HOME/python/:$PYTHONPATH
export PYTHONPATH=$SPARK_HOME/python/lib/py4j-0.8.2.1-src.zip:$PYTHONPATH
export PATH=$JAVA_HOME/bin:$PATH"
salt-ssh '*' "curl http://d3kbcqa49mib13.cloudfront.net/spark-1.4.1-bin-hadoop2.6.tgz | tar -zx -C /usr/local --show-transformed --transform='s,/*[^/]*,spark,'"
salt-ssh 'master' "cat <<_EOF>> /usr/local/spark/conf/slaves
master
slave1
slave2
slave3
slave4
slave5
slave6
slave7
slave8"

echo 'Please ssh to the master node and startup the spark cluster by running $SPARK_HOME/sbin/start-all.sh'
