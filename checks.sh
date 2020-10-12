#!/bin/bash

pyfiles=$(find -type f | grep .py | grep -v 'pycache' | grep -v 'build' | grep -v 'mypy')

if [ "$pyfiles" ]
then
  black $pyfiles
fi

