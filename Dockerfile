# Create the image based on the ibmfunctions image so all of the openwhisk properties are already included
FROM ibmfunctions/action-python-v3.7

# Install these libraries so the classifier can use them inside the docker instance
RUN pip install --progress-bar=on --upgrade pip tensorflow numpy

# Assumes the needed models are in their default path, and copies them into the docker image
COPY models/ /root/.keras/models/
