#!/usr/bin/env bash

# A script for checking "control status" of open-falcon compoents in container

main () {
	container_list="agent aggregator alarm dashboard fe graph hbs judge links nodata portal query sender task transfer"
	echo "Checking the following containers: ${container_list}."
	for i in $container_list; do
		check_control $i
	done
}


check_control() {
	container=$1
	output=$(docker exec $container /home/$container/control status)

	# Check the exit status of last command
	if [[ $? != 0 ]]; then
		echo "[ERROR] $container"
	# Match the substring in the output
	elif [[ $output == *"stoped"* ]]; then
		echo "[STOP!] $container"
	else
		echo "[PASS.] $container"
	fi
}

main
