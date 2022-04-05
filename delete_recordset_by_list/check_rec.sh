#!/bin/bash
#$1 - check the list
#$2 - type of zone ("a" or "ptr")
#set -x
while read p1 p2 p3; do
    [[ "$p1" =~ ^#.*$ ]] && continue
    echo '==========================='
    echo 'is '$p1' in use?'
    fip=$(openstack floating ip list --fixed-ip-address $p1)
    if [[ -z "$fip" ]]
    then
      echo 'no'
    else
      break
    fi
    echo 'get recordset id by zone_id'
    if [[ "$2" == "ptr" ]]
    then
    rec_id=$(openstack recordset list -c id -c records -f value --all-projects $p2 | grep $p3 | cut -d " " -f1)
    fi
    if [[ "$2" == "a" ]]
    then
    rec_id=$(openstack recordset list -c id -c name -f value --all-projects $p2 | grep $p3 | cut -d " " -f1)
    fi
    echo $rec_id
    echo 'deleting record'
    openstack recordset delete --all-projects $p2 $rec_id
    echo 'is recordset deleted?'
    rec=$(openstack recordset list -c id -c records --all-projects $p2 | grep $p3)
    if [[ -z "$rec" ]]
    then
      echo 'yes'
    else
      echo $rec
    fi
done < $1
