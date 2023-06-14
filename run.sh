#!/bin/bash

xterm -e "python3 meteo_wroker.py" &
xterm -e "python3 meteo_wroker.py" &
xterm -e "python3 meteo_wroker.py" &

xterm -e "python3 terminal_server.py" &
xterm -e "python3 terminal_server.py" &


sleep 3

xterm -e "python3 proxy.py" &

sleep 3

for i in {1..50}
do
    python3 air_client.py
    python3 poll_client.py
    sleep 1
done

print("Yo creo que esta de 10")