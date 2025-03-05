#!/bin/bash
# printf "\033]52;c;%s\007" "$(base64 | tr -d '\n')"

if ! test -p /dev/stdin; then
    echo "no pipe detected"
    exit 1
fi

printf "\033]52;c;%s\007" "$(base64 | tr -d '\n')"
