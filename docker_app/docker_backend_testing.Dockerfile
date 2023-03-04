FROM python:3.9.16-alpine3.17

ARG DB_CONTAINER_HOSTNAME
ARG MYSQL_GUEST_PORT

RUN apk add --no-cache  \
    build-base  \
    linux-headers \
    dos2unix \
    vim

# Set the working directory in the container
WORKDIR /DevOpsExpertsProj
COPY ../src /DevOpsExpertsProj/src
COPY ../requirements.txt /DevOpsExpertsProj/requirements.txt
COPY ../backend_testing_start.sh /DevOpsExpertsProj/backend_testing_start.sh

# dos2unix - change file encoding
RUN dos2unix backend_testing_start.sh

# change start.sh file permissions
RUN chmod +x backend_testing_start.sh

RUN python -m pip install --upgrade pip
RUN pip install --ignore-installed --trusted-host pypi.python.org -r /DevOpsExpertsProj/requirements.txt

CMD ["/bin/sh", "/DevOpsExpertsProj/backend_testing_start.sh"]
