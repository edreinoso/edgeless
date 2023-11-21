read -p "Do you want to deploy? (Y/n) " deployment_option
export component_name=""
export component_version=""

config_path="./greengrass/components/config"

component_file="$config_path/$component_name.json" 
deployment_file="$config_path/deployment.json" 

# Environment variables
component_json=$(envsubst < "$component_file")

# Updating components
curl --location 'http://127.0.0.1:5000/createcomponentversion' \
    --header 'Content-Type: application/json' \
    --data "$component_json"

if [ $deployment_option == "Y" ]; then
    read -p "Description of deployment: " description

    export deployment_description=$description

    deployment_json=$(envsubst < "$deployment_file")

    curl --location 'http://127.0.0.1:5000/createdeployment' \
    --header 'Content-Type: application/json' \
    --data "$deployment_json"
fi
