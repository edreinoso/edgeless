export component_name=""
export component_description=""
export component_version=""
ip_from_your_ip=""


component_path="./greengrass/components/"
config_path="./greengrass/components/config"

# Copy files

scp -R $component_path/native/* pi@$ip_from_your_ip:/path/to/your/pi/$component_name/

aws s3 cp $component_path/native/handler.py s3://path/to/your/bucket/$component_name/$component_version/handler.py

component_file="$config_path/native.json" 

# Environment variables
component_json=$(envsubst < "$component_file")

# Updating components
curl --location 'http://127.0.0.1:5000/createcomponentversion' \
    --header 'Content-Type: application/json' \
    --data "$component_json"
