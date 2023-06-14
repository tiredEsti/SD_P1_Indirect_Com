import redis
import pika, sys, os
import meteo_utils
import pickle


redis_db = redis.Redis(host='localhost', port=6379, db=0)



def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='server_queue')

    def callback(ch, method, properties, body):
        data = pickle.loads(body)

        if isinstance(data, meteo_utils.RawMeteoData):
            processor = meteo_utils.MeteoDataProcessor()
            coef = processor.process_meteo_data(data)
            redis_db.rpush('meteo', f'({data.timestamp} : {coef})')
            print('Wellness data received and stored')
        else:
            processor = meteo_utils.MeteoDataProcessor()
            coef = processor.process_pollution_data(data)
            redis_db.rpush('poll', f'({data.timestamp} : {coef})')
            print('Pollution data received and stored')

    channel.basic_consume(queue='server_queue', on_message_callback=callback, auto_ack=True)

    print('Starting server. Listening for meteo or pollution data...')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
