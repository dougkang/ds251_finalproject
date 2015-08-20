#!/bin/bash

salt-ssh '*' "su - hadoop; echo master >> /usr/local/hadoop/etc/hadoop/masters; echo -e 'master\nslave1\nslave2\nslave3\nslave4\nslave5\nslave6\nslave7\nslave8 >> /usr/local/hadoop/etc/hadoop/slaves'"
salt-ssh '*' "su - hadoop; echo 'export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64/jre' >> /usr/local/hadoop/etc/hadoop/hadoop-env.sh"
salt-ssh '*' "su - hadoop; echo 'export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64/jre' >> /usr/local/hadoop/etc/hadoop/yarn-env.sh"
salt-ssh '*' "su - hadoop; cat << _EOF >> /usr/local/hadoop/etc/hadoop/core-site.xml
<configuration>
<property>
<name>fs.default.name</name>
<value>hdfs://master:9000</value>
</property>
</configuration>
_EOF"
salt-ssh '*' "su - hadoop; cat << _EOF >> /usr/local/hadoop/etc/hadoop/mapred-site.xml
<configuration>
<property>
<name>mapreduce.framework.name</name>
<value>yarn</value>
</property>
</configuration>
_EOF"
salt-ssh '*' "su - hadoop; cat << _EOF >> /usr/local/hadoop/etc/hadoop/hdfs-site.xml
<configuration>
<property>
<name>dfs.replication</name>
<value>3</value>
</property>
<property>
<name>dfs.data.dir</name>
<value>/data</value>
</property>
</configuration>
_EOF"
salt-ssh '*' "su - hadoop; cat << _EOF >> /usr/local/hadoop/etc/hadoop/yarn-site.xml
<configuration>
<property>
<name>yarn.nodemanager.aux-services</name>
<value>mapreduce_shuffle</value>
</property>
<property>
<name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name>
<value>org.apache.hadoop.mapred.ShuffleHandler</value>
</property>
<property>
<name>yarn.resourcemanager.resource-tracker.address</name>
<value>master:8025</value>
</property>
<property>
<name>yarn.resourcemanager.scheduler.address</name>
<value>master:8030</value>
</property>
<property>
<name>yarn.resourcemanager.address</name>
<value>master:8050</value>
</property>
</configuration>
_EOF"
salt-ssh 'master' 'hadoop namenode -format'
