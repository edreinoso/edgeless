import boto3

client = boto3.client('greengrassv2')

list = ['lambda_nocontainer_nopinned']

for n in range(len(list)):
    response = client.list_component_versions(
        arn=f'arn:aws:greengrass:eu-central-1:109139691401:components:{list[n]}',
    )
    num_versions = len(response['componentVersions'])

    print(list[n], num_versions)
    
    for i in range(num_versions):
        print(response['componentVersions'][i]['arn'])
        component_arn = response['componentVersions'][i]['arn']
        client.delete_component(
            arn=component_arn
        )



# gg = boto3.client('iot-data')

# message='hello from lambda'
# topic = 'thesis/start'

# gg.publish(
#     topic=topic,
#     payload=message.encode(),
# )