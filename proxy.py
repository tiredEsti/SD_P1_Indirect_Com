import redis
import pika, sys, os
import pickle
from datetime import datetime
import time
import meteo_utils
# Redis connection
r = redis.Redis(host='localhost', port=6379, db=0)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

# Tumbling window size in seconds
Y = 5
# Function to calculate mean of coefficients in a list
def calculate_mean(lst):
    return sum(lst) / len(lst)

# Function to get data from Redis return calculate mean and timestamp
def get_data(data):
    coeff = r.rpop(data)
    if coeff is None:
        return [None, None]
    ts = coeff.decode().split(" : ")[0].strip('(')
    list = []
    while True:
        value = float(coeff.decode().split(" : ")[1].strip(')'))
        list.append(value)
        coeff = r.rpop(data)
        if coeff is None:
            break
    return [calculate_mean(list), ts]

# Main loop
try:
    while True:   
        time.sleep(Y)
        wdata = get_data('meteo')
        pdata = get_data('poll')
        # Send mean to connected terminals
        data = meteo_utils.ProcessedData(wdata[0], pdata[0], wdata[1], pdata[1])
        p_data = pickle.dumps(data)
        channel.basic_publish(exchange='logs', routing_key='terminal_queue', body= p_data)
        print("Data retrieved from Redis and sent to terminals")
except KeyboardInterrupt:
    connection.close()
    exit(0)

