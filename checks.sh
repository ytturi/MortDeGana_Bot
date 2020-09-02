#!/bin/bash

pyfiles=$(find -type f | grep .py | grep -v 'pycache' | grep -v 'build')

if [ "$pyfiles" ]
then
  black $pyfiles
fi

