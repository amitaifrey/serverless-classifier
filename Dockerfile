FROM ibmfunctions/action-python-v3.7

RUN pip install --progress-bar=on --upgrade pip tensorflow numpy
COPY models/ /root/.keras/models/
