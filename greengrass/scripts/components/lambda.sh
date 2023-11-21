export component_name=""
export function_name=""
export component_version=""

# Paths
lambda_path="./greengrass/components/lambda"
config_path="./greengrass/components/config"

lambda_component_file="$config_path/lambda/$component_name.json" 

# Lambda Operations
cd $lambda_path

zip -r function.zip lambda_function.py classification.py reduction.py

aws lambda update-function-code --function-name $function_name --zip-file fileb://function.zip --no-cli-pager

# Sleeper time for function update
sleep 3

# Invoke publish-version and store the output in a variable
output=$(aws lambda publish-version --function-name $function_name)

# Extract the Version using jq (a JSON processor)
export function_version=$(echo $output | jq -r '.Version')

echo $function_version


# Environment variables
lambda_component_json=$(envsubst < "$lambda_component_file")


# Making call to the web server
curl --location 'http://127.0.0.1:5000/createlambdacomponentversion' \
    --header 'Content-Type: application/json' \
    --data "$lambda_component_json"
