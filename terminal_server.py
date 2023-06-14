
import pika, sys, os
import pickle
from datetime import datetime
import time
import meteo_utils

import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='logs', exchange_type='fanout')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='logs', queue=queue_name)

    # create a figure and axis object
    fig = plt.figure(figsize = (7, 5))
    ax = fig.add_subplot(2,1,1)
    ax.set_title('Wellness and pollution data')
    ax.set_xlabel('Time')
    ax.set_ylabel('Coefficient')

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))

    # initialize the x and y data arrays
    wtime = []
    ptime = []
    wcoef = []
    pcoef = []

    # create a line plot of the wellness and pollution data
    wellness_line, = ax.plot(wtime, wcoef, color='purple', label='Wellness')
    pollution_line, = ax.plot(ptime, wcoef, color='cyan', label='Pollution')
    ax.legend()
    
    # create a callback function which is called when a message is received
    def callback(ch, method, properties, body):
        data = pickle.loads(body)

        if data.timestampWell is not None:
            wcoef.append(data.well)
            wtime.append(datetime.strptime(data.timestampWell, '%Y-%m-%d %H:%M:%S'))
        if data.timestampPoll is not None:
            pcoef.append(data.poll)
            ptime.append(datetime.strptime(data.timestampPoll, '%Y-%m-%d %H:%M:%S'))
        # update the line plot with the new data
        wellness_line.set_data(wtime, wcoef)
        pollution_line.set_data(ptime, pcoef)

        # set the x-axis limits to show the most recent data
        #ax.set_xlim(len(wcoef)-10, len(wcoef))
        # Rotating X-axis labels
        for tick in ax.get_xticklabels():
            tick.set_rotation(90)
        ax.relim()
        ax.autoscale_view()
        fig.canvas.draw()
        print("updated")
        # pause the plot for a short duration before updating it with new data
        plt.pause(5)
    
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
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