import json
import time
import argparse
import os
from datetime import datetime
from throughput import ThroughputExp

throughput_exp_class = ThroughputExp()

def write_json(file_path, file_name, data, env):
    if not os.path.exists(file_path):
        print(f"Creating new directory output data for {env}!\n")
        os.mkdir(file_path)

    with open(f'{file_path}/{file_name}', 'w') as file:
        file.write(','.join(map(str, data)))

def execution_environment(start_time, url, key_list, env):
    time_array = throughput_exp_class.sequential_test(start_time, url, key_list, env)
    
    end_time = time.time()
    execution_time_seconds = end_time - start_time
    print(f"Execution Time: {execution_time_seconds:.6f}\n")
    return time_array

def main():
    print('\nstart time:',datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'\n')
    sequential_time_array = []
    service_time_array = []

    url = {
        "lambdas": 'https://custom_domain_name/lambdas',
        "fargate": 'https://custom_domain_name/fargate',
    }

    key_list = []

    parser = argparse.ArgumentParser(
        description='Load test script for signal processing workload.')
    parser.add_argument('--requests', type=str, default="",
                        help='Number of requests')
    parser.add_argument('--repetitions', type=str, default="",
                        help="Sorting variable by")
    parser.add_argument('--runtime', type=str, default="",
                        help="Runtime environment")

    args = parser.parse_args()

    requests = args.requests
    repetitions = int(args.repetitions)
    runtime = args.runtime

    dir = os.environ.get(f'local_directory_{requests}')

    for filename in os.listdir(dir):
        if filename.endswith(".wav"):
            s3_key = f'unsorted/{requests}/{filename}'
            
            key_list.append(s3_key)

    if (runtime == "lambda"):
        # """
        print("STARTING LAMDBA SEQUENTIAL EXPERIMENT\n======================\n")
        sequential_start_time = time.time()
        print(f'Lambda Sequential: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        for n in range(0, repetitions):
            sequential_time_array.append(execution_environment(sequential_start_time, url['lambdas'], key_list, 'lambdas'))
        # """
        date_dir = datetime.now().strftime("%d_%m_%Y")
        time_dir = datetime.now().strftime("%H:%M:%S")
        write_json(f'./out/execution/sequential/{date_dir}', f'{repetitions*100}_{time_dir}.txt', sequential_time_array, 'Lambda Function')
    else:
        """
        print("STARTING FARGATE (TASKS) SEQUENTIAL EXPERIMENT\n======================\n")
        task_start_time = time.time()
        print(f'Fargate Sequential: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        task_temp_array = []
        for n in range(0, repetitions):
            task_temp_array.append(execution_environment(task_start_time, url['fargate'], key_list, 'task', concurrency))
        task_time_array = task_time_array
        """

        # """
        print("STARTING FARGATE (SERVICE) SEQUENTIAL EXPERIMENT\n======================\n")
        service_start_time = time.time()
        print(f'Fargate Sequential: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        for n in range(0, repetitions):
            service_time_array.append(execution_environment(service_start_time, url['fargate'], key_list, 'service'))
        # """
        date_dir = datetime.now().strftime("%d_%m_%Y")
        time_dir = datetime.now().strftime("%H:%M:%S")
        write_json(f'./out/execution/service/{date_dir}', f'{repetitions*100}_{time_dir}.txt', service_time_array, 'Flask Docker Container')    

    print('end time:',datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'\n')

if __name__ == '__main__':
    main()
