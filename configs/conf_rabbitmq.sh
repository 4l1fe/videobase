#!/bin/bash
docker_ip=$(ifconfig docker0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}')
#if docker_ip == ""
#    then

echo $docker_ip
