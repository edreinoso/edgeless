read -p "Description of deployment: " description
# read -p "Version of components to deploy: " version

export deployment_description=$description
# export component_version=$version

config_path="/Users/elchoco/ms_cs/academics/2y/Thesis/mastergit/greengrass/components/config"

deployment_file="$config_path/deployment.json" 

deployment_json=$(envsubst < "$deployment_file")

# cat $deployment_json

curl --location 'http://127.0.0.1:5000/createdeployment' \
    --header 'Content-Type: application/json' \
    --data "$deployment_json"