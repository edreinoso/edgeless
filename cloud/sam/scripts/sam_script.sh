# build project
sam build

# deploy the whole setup
sam deploy --parameter-overrides SignalImage=$1 CertificateArn=$certarn