import concurrent.futures
import json
import time
import requests
from datetime import datetime
from ecs import ECS

class ThroughputExp:
    def __init__(self):
        self.bucket_name = "cloud-signal-throughput-experiment"
        self.time_taken_sequential = []
        self.fargate_sequential = []
        self.time_taken_concurrent = []
        self.ecs_fargate = ECS()

    def send_signal_over_http(self, exp_start_time, url, key, env):
        payload = {'bucket': self.bucket_name, 'key': key, 'env': env}

        try:
            start_time = time.time()
            response = requests.post(url, json=payload)
            end_time = time.time()
            if response.status_code == 200:
                total_execution_time = end_time - exp_start_time
                # total_execution_time = end_time - start_time
                res = json.loads(response.text)
                if (env == 'lambdas' or env == "service"):
                    print(f"Sequential Process Time: {total_execution_time} seconds")
                elif (env == 'lambdac'):
                    print(f"Concurrent Process Time: {total_execution_time} seconds")
                
                return total_execution_time
            else:
                print(f"HTTP request error: {response.status_code} from file {key}")
        except Exception as e:
            print(f"Error sending HTTP request: {e} from file {key}")

    def send_signal_to_fargate(self, iteration_num, exp_start_time, key):
        return_time = self.ecs_fargate.run_task(key)
        total_execution_time = return_time - exp_start_time

        print(f"{iteration_num}. Fargate Process Time: {total_execution_time} seconds")

        return total_execution_time
        

    def load_test(self, url, exp_start_time, concurrency_res, batch_payload):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.send_signal_over_http, exp_start_time, url, payload, 'lambdac')
                        for payload in batch_payload]
            concurrent.futures.wait(futures)

            for future in futures:
                response = future.result()
                concurrency_res.append(response)
        
        return concurrency_res

    def sequential_test(self, exp_start_time, url, key_list, env):
        self.time_taken_sequential = []
        if (env == "lambdas" or env == "service"):
            for n in range(0,len(key_list)):
                self.time_taken_sequential.append(self.send_signal_over_http(exp_start_time, url, key_list[n], env))
            
            return self.time_taken_sequential
        else:
            for n in range(0,len(key_list)):
                self.fargate_sequential.append(self.send_signal_to_fargate(exp_start_time, key_list[n]))
            return self.fargate_sequential     

    def concurrent_test(self, exp_start_time, url, key_list, concurrency):
        num_batches = len(key_list) // concurrency
        print(len(key_list), num_batches, concurrency)

        concurrency_res = []

        for batch_index in range(num_batches): 
            batch_start = batch_index * concurrency
            batch_end = batch_start + concurrency
            batch_payloads = key_list[batch_start:batch_end]
            print('checking out the payload',batch_payloads, 'and length', len(batch_payloads))
            self.time_taken_concurrent = self.load_test(url, exp_start_time, concurrency_res, batch_payloads)
            end_time = time.time()
            total_time = end_time - exp_start_time
        
        return self.time_taken_concurrent
