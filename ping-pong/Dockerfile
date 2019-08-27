FROM gcr.io/google-appengine/python
LABEL python_version=python3.7

# create a virtualenv for dependencies
RUN virtualenv -p python3.7 /env

# update pip
RUN pip install --upgrade pip

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Expose server port
EXPOSE 8001

ENTRYPOINT [ "python" ]

CMD [ "ping-pong.py" ]
