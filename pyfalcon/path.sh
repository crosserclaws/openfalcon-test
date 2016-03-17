#!/usr/bin/env bash

if [ -z $PYTHONPATH ]; then
  export PYTHONPATH=`pwd`
else
  export PYTHONPATH=$PYTHONPATH:`pwd`
fi


