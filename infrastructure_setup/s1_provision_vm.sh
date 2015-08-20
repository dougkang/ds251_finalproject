for host in master slave1 slave2 slave3 slave4 slave5 slave6 slave7 slave8
do
    echo "provisioning ${host}"
    slcli vs -y create -D w251.final -H ${host} -c 2 -m 16384 -o UBUNTU_LATEST_64 -d dal09 -k key-tma --disk 25 --disk 300 -n 1000
    sleep 10
done

echo "run slcli vs list to make sure VMs are ready before continuing..."
