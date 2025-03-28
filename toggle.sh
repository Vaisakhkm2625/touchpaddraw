#!/bin/bash

if [ -f .tpd-pid ]; then
    PID=$(cat .tpd-pid)

    pkill dotoold    
    pkill -TERM -P $PID
    kill -9 $PID 2>/dev/null

    rm .tpd-pid
else
    ./start.sh &
    echo $! > .tpd-pid
fi
