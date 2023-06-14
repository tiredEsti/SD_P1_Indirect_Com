#!/bin/bash

#sudo docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.12-managemen

xterm -e "python3 meteo_worker.py" &
xterm -e "python3 meteo_worker.py" &
xterm -e "python3 meteo_worker.py" &

xterm -e "python3 proxy.py" &


xterm -e "python3 terminal_server.py" &
xterm -e "python3 terminal_server.py" &


for i in {1..50}
do
    python3 air_client.py
    python3 poll_client.py
    sleep 1
done

print("Yo creo que esta de 10")