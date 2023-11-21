import json
import os
import threading
import traceback
import time
from datetime import datetime

import awsiot.greengrasscoreipc.clientv2 as clientV2

start_topic = 'thesis/core/w2'
qos = '1'

ipc_client = clientV2.GreengrassCoreIPCClientV2()

def subscribe_runtime_mqtt(event):
    try:
        date_dir = datetime.now().strftime("%d_%m_%Y")
        time_dir = datetime.now().strftime("%H:%M:%S")
        
        # init classes
        message = str(event.message.payload, 'utf-8')
        
        end_time = time.time()

        data = json.loads(message)

        total_execution_time = end_time - data['start_time']

        env = data['environment']
        size = data['size']

        write_json(f'/path/to/directory/{date_dir}/{env}/w2', f'{size}.txt', total_execution_time, env)

    except:
        traceback.print_exc()

def write_json(file_path, file_name, data, env):
    if not os.path.exists(file_path):
        print(f"Creating new directory output data for {env}!\n")
        os.mkdir(file_path)

    with open(f'{file_path}/{file_name}', 'a') as file:
        file.write(f"{data},")

def on_stream_error(error):
    # Return True to close stream, False to keep stream open.
    return True  

def on_stream_closed():
    pass

def main():
    print('Successfully subscribed to start experiment: ' + start_topic)
    
    _, runtime = ipc_client.subscribe_to_iot_core(
        topic_name=start_topic,
        qos=qos, 
        on_stream_event=subscribe_runtime_mqtt,
        on_stream_error=on_stream_error,
        on_stream_closed=on_stream_closed
    )
    print('Successfully subscribed to runtime enviornment: ' + start_topic)
    
    # Keep the main thread alive, or the process will exit.
    event = threading.Event()
    event.wait()

    # To stop subscribing, close the operation stream.
    runtime.close()
    ipc_client.close()

if __name__ == "__main__":   
    main()