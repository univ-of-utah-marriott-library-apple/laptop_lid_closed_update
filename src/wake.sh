#!/bin/bash

name=$1
mac=$2
ip=$3
# 	echo "mac: $mac"
ping -c 1 -W 1 $ip > /dev/null 2> /dev/null;
if [ $? -eq 0 ]; then
#   arp -n -i eth0 $ip | grep ether >> ARPResults
    wakeonlan.pl "$mac"
    echo 'success'
#	&& sleep 3 && ssh mac@$ip touch /tmp/radmind
else
	echo "failure: $1 $2 $3";

fi

exit 0

#sleep 30

# while read line
# do
#     ip=$(awk '{print $2}' "$line")
#     echo -e "ip: $ip\n"
# done < $1

