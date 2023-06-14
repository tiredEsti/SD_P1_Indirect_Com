# Description: Client for the air quality service
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
air = detector.analyze_air()
currenttime = datetime.now()
air_info = meteo_utils.RawMeteoData(air['temperature'], air['humidity'], currenttime.strftime("%Y-%m-%d %H:%M:%S"))

p_air_info = pickle.dumps(air_info)

channel.basic_publish(exchange='', routing_key='server_queue', body= p_air_info)

print("Air data added")

connection.close()
