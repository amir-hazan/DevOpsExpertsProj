#!/bin/bash

wait_for_db() {
  host="$1"
  port="$2"

  echo "Waiting for $host:$port to become available..."

  while ! nc -z "$host" "$port"; do
    sleep 1
  done

  echo "$host:$port is now available, continuing with the script..."
}

check_file_exist () {
  if [ ! -f "$1" ];
  then
    echo "$1 does not exist."
    exit 1
  else
    echo "***** $1 exists. *****"
    dos2unix $1
  fi
}

wait_for_db "$DB_CONTAINER_HOSTNAME" "$MYSQL_GUEST_PORT"

check_file_exist "src/testings/docker_backend_testing.py"

/bin/sh -c "sleep 3 && python src/testings/docker_backend_testing.py"
