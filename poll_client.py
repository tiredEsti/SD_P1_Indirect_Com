# Description: Client that sends pollution data to the server
from datetime import datetime
import pickle
import pika

import meteo_utils

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='server_queue')

detector = meteo_utils.MeteoDataDetector()

# create a valid request message
poll = detector.analyze_pollution()
currenttime = datetime.now()
poll_info = meteo_utils.RawPollutionData(poll['co2'], currenttime.strftime("%Y-%m-%d %H:%M:%S"))

p_poll_info = pickle.dumps(poll_info)

channel.basic_publish(exchange='', routing_key='server_queue', body= p_poll_info)

print("Pollution data added")

connection.close()