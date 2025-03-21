#!/bin/bash
if [ "$#" -eq 0 ]; then
  echo "Usage: $0 command"
  exit 1
fi

"$@" > >(sed $'s/^/\e[32mSTDOUT:\e[0m /') 2> >(sed $'s/^/\e[31mSTDERR:\e[0m /' >&2)
