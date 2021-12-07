#!/bin/bash

PRJ=$1
if [[ -z "$PRJ" ]]; then
  echo "Please set project ID or Name"
  exit 1
fi

function show_prj_object () {
  OBJ=$(openstack $1 list --project "$PRJ" -f yaml)
  if [ $? -eq 1 ]; then
   exit 1
  fi
  echo "$2 list:"
  [[ -z "$OBJ" ]]&&echo "0"||echo $OBJ
}

## "User list"
show_prj_object "user" "User"

## "Volume list"
show_prj_object "volume" "Volume"

## "Instance list"
show_prj_object "server" "Instance"

## "Network list"
show_prj_object "network" "Network"

## "Subnet list"
show_prj_object "subnet" "Subnet"

## "Router list"
show_prj_object "router" "Router"

## "FLoating IP list"
show_prj_object "floating ip" "Floating IP"

## "Security Group list"
show_prj_object "security group" "Security Group"

## "Loadbalancer list"
show_prj_object "loadbalancer" "LoadBalancer"

## "Port list"
show_prj_object "port" "Port"
