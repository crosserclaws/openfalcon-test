#!/usr/bin/env bash

# A POSIX variable
OPTIND=1         # Reset in case getopts has been used previously in the shell.

# Initialize variables
container_list="agent aggregator alarm dashboard fe graph hbs judge links nodata portal query sender task transfer"
callback=""
sub_command=""
options=""
args=""
verbose=false

#
#
# Utility function
#
#
function msg() {
  skip=${1}+1
  echo "[$2][${FUNCNAME[$skip]}] ${@:3}" >&2
}

function vmsg() {
  if $verbose ; then
    msg ${1}+1 "${@:2}"
  fi
}

function invalid_option() {
  msg 1 "ERR" "Invalid option: $@"
}

function require_option() {
  msg 1 "ERR" "Option $@ requires an argument."
}

function usage() {
  echo "[MSG] The script provides some useful utilities in testing env."
  echo "      $0 [sub_command] [options...] [args...]"
  echo "      -h             Print usage"
  echo "      -e=native      Env type = {native, docker, kvm}"
  exit 0
}

function parse() {
  while getopts ":slurpcft:hv" opt; do
    case $opt in
      #
      # [Sub_command]
      #
      # docker-compose
      u)
        sub_command="up"
        ;;
      r)
        sub_command="remove"
        ;;
      p)
        sub_command="pause"
        ;;
      # docker exec
      s)
        sub_command="status"
        ;;
      # docker logs
      l)
        sub_command="logs"
        ;;
      # clean-up /home/openfalcon/* 
      c)
        sub_command="clean"
        ;;
      #
      # [Option]
      #
      f)
        options+="-f "
        ;;
      t)
        options+="--tail=$OPTARG "
        ;;
      h)
        usage
        ;;
      v)
        verbose=true
        vmsg 0 "MSG" "${!verbose@}: $verbose"
        ;;
      \?)
        invalid_option "-$OPTARG"
        exit 1
        ;;
      :)
        require_option "-$OPTARG"
        exit 1
        ;;
    esac
  done
}

function is_substring() {
  sub=$1
  str=${@:2}
  if [[ "$str" == *"$sub"* ]]; then
    return 1
  fi
  return 0
}

# Do callback for each container
function ioc() {
  vmsg 1 "MSG" "${FUNCNAME[0]}() the following containers: $@."
  for i in $@; do
    is_substring "$i" "$container_list"
    # Check func's return value
    if [[ $? == 1 ]]; then
      eval $callback $i
    fi
}

function status_one() {
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

function status() {
  callback=status_one
  # All container
  if [[ $1 == "" ]]; then
    ioc $container_list
  else
    # Some containers
    ioc $@
  fi
}

function log_one() {
  container=$1
  docker logs $options $container
}

function log() {
  if [[ $# == 0 ]]; then
    msg 0 "ERR" "Invalid sub_command [$sub_command] and args [$args]"
    return
  fi
  # Some containers
  callback=log_one
  ioc $@
}

function clean_one() {
  container=$1
  sudo rm -r $options /home/openfalcon/$container
}

function clean() {
  callback=clean_one
  ioc $@
}

function compose() {
  cmd=$1
  opt=${@:2}
  # Default
  if [[ $options == "" ]]; then
    docker-compose $cmd $opt
  # -f init.yml
  elif [[ $options == "-f " ]]; then
    docker-compose -f init.yml $cmd $opt
  else
    msg 0 "ERR" "[$sub_command]: args [$args]"
  fi
}

#
#
# Main function
#
#

function main() {
  parse $@

  # Shift params & print msgs
  vmsg 0 "MSG" "${!sub_command@}: [$sub_command]"
  vmsg 0 "MSG" "${!options@}: [$options]"
  shift $((OPTIND-1))
  args=$@
  vmsg 0 "MSG" "${!args@}: [$args]"

  case $sub_command in
    status)
      status $args
      ;;
    logs)
      log $args
      ;;
    clean)
      clean $args
      ;;
    up)
      compose "up" "-d"
      ;;
    pause)
      compose "stop"
      ;;
    remove)
      compose "rm" "-f"
      ;;
    *)
      msg 0 "ERR" "Invalid sub_command [$sub_command] and args [$args]"
      ;;
  esac

}

main $@

# End of file