for host in master slave1 slave2 slave3 slave4
do
    echo "provisioning ${host}"
    yes | slcli vs create -D w251.final -H ${host} -c 2 -m 4096 -o UBUNTU_LATEST_64 -d dal09 -k key-tma --disk 25 --disk 100 -n 1000
    sleep 10
done

echo "run slcli vs list to make sure VMs are ready before continuing..."
