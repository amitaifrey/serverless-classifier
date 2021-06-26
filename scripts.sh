# Create the cloud function with 512MB of RAM and web requests enabled
ibmcloud fn action create classify --docker amifre/serverless-classifier:0.1 action.py --web true --memory 512

# Delete the cloud function
ibmcloud fn action delete classify

# Invoke the cloud function through the CLI with params.json containing the base64 image
ibmcloud fn action invoke --result classify --param-file params.json

# Invoke the cloud function's REST API with params.json containing the base64 image
curl -v -u <username>:<password> -d @params.json -H "Content-Type: application/json" -X POST https://eu-gb.functions.cloud.ibm.com/api/v1/namespaces/amifre%40gmail.com_dev/actions/classify?blocking=true

# Get live logs of cloud function activations
ibmcloud fn activation poll