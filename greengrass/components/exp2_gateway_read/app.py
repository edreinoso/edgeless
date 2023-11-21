import json
import os
import boto3
import sys
import concurrent.futures
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

start_topic = 'thesis/start/w2'
qos = '1'
# delete soon
topic_pub_sub = 'white/green'

ipc_client = clientV2.GreengrassCoreIPCClientV2()

## SUBSCRIBE TO TOPIC

def load_test(topic, filename, env, threads, start_time):
    # Iterating through each of the directory
    dict_signal = {
        'file': filename,
        'env': env,
        'size': threads,
        'topic': 'thesis/core/w2',
        'start_time': start_time
    }

    signal = json.dumps(dict_signal)
    print('processed signal',signal)

    # Local MQTT
    publish_binary_message_to_topic(ipc_client, topic, signal)

def subscribe_start_exp_mqtt(event):
    try:
        # init classes
        message = str(event.message.payload, 'utf-8')

        data = json.loads(message)

        print(data['topic'], data['size'])

        topic = data['topic']
        env = data['env']
        num_threads = int(data['size'])

        key_list = []

        directory="/path/to/audio/files"

        # putting all the files in a list
        for filename in os.listdir(directory):
            if filename.endswith(".wav"):
                key_list.append(filename)

        num_batches = len(key_list) // num_threads

        start_time = time.time()

        for batch_index in range(num_batches):
            batch_start = batch_index * num_threads
            batch_end = batch_start + num_threads
            batch_payload = key_list[batch_start:batch_end]

            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(load_test, topic, payload, env, num_threads, start_time)
                            for payload in batch_payload]
                concurrent.futures.wait(futures)

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