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
      c)
        sub_command="clean"
        ;;
      # docker exec
      s)
        sub_command="status"
        ;;
      # docker logs
      l)
        sub_command="logs"
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
    vmsg 0 "MSG" "[$sub] is in [$str]"
    return 1
  fi
  vmsg 0 "MSG" "[$sub] is not in [$str]"
  return 0
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

function ioc() {
  # All container
  if [[ $1 == "all" ]]; then
    # Msgs & shift
    vmsg 0 "MSG" "Pre- shift $@"
    shift
    vmsg 0 "MSG" "Post-shift $@"
    # :~)

    msg 0 "MSG" "${FUNCNAME[0]}() the following containers: ${container_list}."
    for i in $container_list; do
      callback $i
    done
    return
  fi

  # A specific container
  vmsg 0 "MSG" "Params to check [$@]"
  for i in $@; do
    is_substring "$i" "$container_list"
    # Check func's return value
    if [[ $? == 1 ]]; then
      callback $i
    fi
  done
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
      callback=status_one
      ioc $args
      ;;
    logs)
      callback=log_one
      ioc $args
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
    clean)
      # OWL
      options=""
      compose "stop"
      compose "rm" "-f"
      # -f init.yml
      options="-f "
      compose "stop"
      compose "rm" "-f"
      ;;
    *)
      msg 0 "ERR" "Invalid sub_command [$sub_command] and args [$args]"
      ;;
  esac

}

main $@

# End of file