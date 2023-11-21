import json
import os
import boto3
import sys
import threading
import traceback
import time
from datetime import datetime

import awsiot.greengrasscoreipc.clientv2 as clientV2
from awsiot.greengrasscoreipc.model import (
    PublishMessage,
    SubscriptionResponseMessage,
    BinaryMessage,
    UnauthorizedError
)

start_topic = 'thesis/start/w1'
qos = '1'
# delete soon
topic_pub_sub = 'white/green'

ipc_client = clientV2.GreengrassCoreIPCClientV2()

## SUBSCRIBE TO TOPIC

def subscribe_start_exp_mqtt(event):
    try:
        # init classes
        message = str(event.message.payload, 'utf-8')

        data = json.loads(message)

        print(data['topic'])

        env = data['env']
        size = data['size']
        repetitions = int(data['size']) / 100

        directory="/path/to/audio/files"

        print(f'Directory where files are located: {directory}, and Repetitions: {repetitions}')

        start_time = time.time()

        # Iterating through each of the directory
        for n in range(0, int(repetitions)):
            for filename in os.listdir(directory):
                if filename.endswith(".wav"):
                    
                    dict_signal = {
                        'file': filename,
                        'env': env,
                        'size': size,
                        'topic': 'thesis/core/w1',
                        'start_time': start_time
                    }

                    signal = json.dumps(dict_signal)

                    # print(signal)

                    # Local MQTT
                    publish_binary_message_to_topic(ipc_client, data['topic'], signal)

    except:
        traceback.print_exc()

## PUBLISH MESSAGES

def publish_binary_message_to_topic(ipc_client, topic, message):
    binary_message = BinaryMessage(message=bytes(message, 'utf-8'))
    publish_message = PublishMessage(binary_message=binary_message)
    return ipc_client.publish_to_topic(topic=topic, publish_message=publish_message)

def on_stream_error(error):
    # Return True to close stream, False to keep stream open.
    return True  

def on_stream_closed():
    pass

def main():
    _, gateway = ipc_client.subscribe_to_iot_core(
        topic_name=start_topic,
        qos=qos, 
        on_stream_event=subscribe_start_exp_mqtt,
        on_stream_error=on_stream_error,
        on_stream_closed=on_stream_closed
    )
    print('Successfully subscribed to start experiment: ' + start_topic)
    
    # Keep the main thread alive, or the process will exit.
    event = threading.Event()
    event.wait()

    # To stop subscribing, close the operation stream.
    gateway.close()
    ipc_client.close()

if __name__ == "__main__":   
    main()