# Deploying SAM

The idea is to implement `sam deploy`, but there are two parameters which I have to pass:

1. Signal Image: for the ECS container service
2. CertificateArn: for the Route53 record

`sam deploy --parameter-overrides SignalImage= CertificateArn=`

Additionally, you should also look into the **scripts** directory within this space, to find more on how to deploy the whole setup.

- sam_script: use this one to deploy the infrastructure and sync the files to the s3 bucket
- delete_all: will delete all the files from the s3 bucket and then delete all resources

## Versions

V9 is the lastest version for deployment

## Aliases

These can be useful in the shell prompt

alias samdeploy='path/to/script/directory/sam_script.sh'

This would then run as follows:

`samdeploy v9`