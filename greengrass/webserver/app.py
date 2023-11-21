from flask import Flask, jsonify, request
from json_formatter import JsonFormatter
import json
import boto3


gg_client = boto3.client('greengrass')
ggv2_client = boto3.client('greengrassv2')
s3_client = boto3.client('s3')

app = Flask(__name__)
jsonFormatter = JsonFormatter()

@app.route('/')
def hello():
    return "New changes!!! Viva Venezuela"

GENERAL = """GENERAL"""
@app.route('/listdeployments', methods=['GET'])
def list_deployments():
    target_arn = request.args.get('targetarn')

    response = ggv2_client.list_deployments(
        targetArn=target_arn
    )

    return response

@app.route('/getdeployment', methods=['GET'])
def get_deployment():
    deployment_id = request.args.get('deploymentid')

    response = ggv2_client.get_deployment(
        deploymentId=deployment_id
    )

    return response

@app.route('/createdeployment', methods=['POST'])
def create_deployment():
    payload = request.get_json()

    target_arn = payload['targetArn']
    name = payload['deploymentName']
    components = payload['components']

    print(target_arn, name, components)
    components["aws.greengrass.LogManager"]["configurationUpdate"]["merge"] = jsonFormatter.convert_to_string('logs.json')

    print('\n',components)

    response = ggv2_client.create_deployment(
        targetArn=target_arn,
        deploymentName=name,
        components=components,
    )

    return response

NOT_LAMBDA = """NOT LAMBDA"""

@app.route('/createcomponentversion', methods=['POST'])
def create_component_version():
    # variables
    payload = request.get_json()

    print('hello world',payload)
    
    # encode payload
    bytes = json.dumps(payload).encode('utf-8')

    response = ggv2_client.create_component_version(
        inlineRecipe=bytes,
    )

    return response

LAMBDA = """LAMBDA"""

@app.route('/createlambdadependencyversion', methods=['POST'])
def create_lambda_dependency_version():
    payload = request.get_json()

    print(payload)

    bytes = json.dumps(payload).encode('utf-8')

    response = ggv2_client.create_component_version(
        inlineRecipe=bytes,
    )

    print(response)

    return response

@app.route('/createlambdacomponentversion', methods=['POST'])
def create_lambda_component_version():
    payload = request.get_json()

    print('inside the /createlambdacomponentversion')

    response = ggv2_client.create_component_version(
        lambdaFunction=payload,
    )

    print('after operation')
    
    return response

if __name__ == '__main__':
    app.run(debug=True)