FROM python:3.9.16-alpine3.17

ARG RUN_SERVER
ARG CREATE_SCHEMA_FOR_K8S
ARG DB_CONTAINER_HOSTNAME
ARG MYSQL_GUEST_PORT

# install packages
RUN apk add --no-cache  \
    build-base  \
    linux-headers \
    dos2unix \
    vim

# Set the working directory in the container
WORKDIR /DevOpsExpertsProj

# Copy the app to the container
COPY ../src /DevOpsExpertsProj/src
COPY ../requirements.txt /DevOpsExpertsProj/requirements.txt
COPY ../start.sh /DevOpsExpertsProj/start.sh

# dos2unix - change file encoding
RUN dos2unix start.sh

# change start.sh file permissions
RUN chmod +x start.sh

# Update pip and Install any needed packages specified in requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install --ignore-installed --trusted-host pypi.python.org -r /DevOpsExpertsProj/requirements.txt

# Run the command to start the app
CMD ["/bin/sh", "/DevOpsExpertsProj/start.sh", "$RUN_SERVER", "$CREATE_SCHEMA_FOR_K8S"]
