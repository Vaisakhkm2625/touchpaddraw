#!/bin/sh

if [ $# -eq 0 ]; then
    echo "Usage: ./toggle.sh <device>"
    exit 1
fi

if [ -f .tpd-pid ]; then
    PID=$(cat .tpd-pid)

    pkill dotoold    
    pkill -TERM -P $PID
    kill -9 $PID 2>/dev/null

    rm .tpd-pid
else
    python main.py -d "$1" &
    echo $! > .tpd-pid
fi
