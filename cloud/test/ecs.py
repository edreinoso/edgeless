import boto3
from datetime import datetime
import time

class ECS:
    def __init__(self):
        self.client = boto3.client('ecs')
        # these values are manual, therefore need to be changed everytime during the experiment
        self.task_definition = ''
        self.security_group = ''

    def run_task(self, s3_key):
        response = self.client.run_task(
            cluster='cloud-throughput-experiment',
            launchType='FARGATE',
            networkConfiguration={
                'awsvpcConfiguration': {
                    'subnets': [
                        ''
                    ],
                    'securityGroups': [
                        self.security_group,
                    ],
                    'assignPublicIp': 'ENABLED'
                }
            },
            overrides={
                'containerOverrides': [
                    {
                        'name': 'signal-process',
                        'environment': [
                            {
                                'name': 's3_key',
                                'value': s3_key
                            }
                        ],
                        'cpu': 256,
                        'memory': 512,
                    }
                ],
            },
            tags=[
                {
                    'key': 'date',
                    'value': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                },
            ],
            taskDefinition=self.task_definition
        )

        task_status = response['tasks'][0]['lastStatus']
        task_arn = response['tasks'][0]['taskArn']

        while task_status != 'STOPPED':
            response = self.client.describe_tasks(
                cluster="cloud-throughput-experiment",
                tasks=[
                    task_arn,
                ],
            )

            task_status = response['tasks'][0]['lastStatus']

            time.sleep(0.5) # important: this sleep avoids throttling

        return time.time()
