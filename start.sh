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

check_file_exist "src/rest_server/rest_app.py"
check_file_exist "src/rest_server/web_app.py"
check_file_exist "src/db/create_db_tables.py"
check_file_exist "src/db/create_k8s_schema.py"

if [ -z "$RUN_SERVER" ] || [ -z "$CREATE_SCHEMA_FOR_K8S" ]; then
  RUN_SERVER="backendOnly"
  CREATE_SCHEMA_FOR_K8S="false"
  echo "The variables RUN_SERVER CREATE_SCHEMA_FOR_K8S was not set. Defaulting to backendOnly and false."
fi

if [ "$RUN_SERVER" = "backendOnly" ]; then
  echo "*** Running only backend server on port 5000 ***"
  if [ "$CREATE_SCHEMA_FOR_K8S" = "true" ]; then
    echo "*** running with creating schema for k8s database ***"
    /bin/sh -c "python src/db/create_k8s_schema.py && sleep 5 && python src/rest_server/rest_app.py"
  else
    echo "*** running without creating schema for k8s database ***"
    /bin/sh -c "python src/db/create_db_tables.py && sleep 5 && python src/rest_server/rest_app.py"
  fi
elif [ "$RUN_SERVER" = "webOnly" ]; then
  echo "*** Running only web server on port 5001 ***"
  if [ "$CREATE_SCHEMA_FOR_K8S" = "true" ]; then
    echo "*** running with creating schema for k8s database ***"
    /bin/sh -c "python src/db/create_k8s_schema.py && sleep 5 && sleep 5 && python src/rest_server/web_app.py"
  else
    echo "*** running without creating schema for k8s database ***"
    /bin/sh -c "python src/db/create_db_tables.py && sleep 5 && python src/rest_server/web_app.py"
  fi
elif [ "$RUN_SERVER" = "bothServers" ]; then
   echo "*** Running both backend and web servers on port 5000 / 5001 ***"
   if [ "$CREATE_SCHEMA_FOR_K8S" = "true" ]; then
    echo "*** running with creating schema for k8s database ***"
     /bin/sh -c "python src/db/create_k8s_schema.py && sleep 5 && python src/rest_server/rest_app.py & sleep 3 & python src/rest_server/web_app.py"
    else
    echo "*** running without creating schema for k8s database ***"
      /bin/sh -c "python src/db/create_db_tables.py && sleep 5 && python src/rest_server/rest_app.py & sleep 3 & python src/rest_server/web_app.py"
    fi
else
  echo "Error: Invalid option for RUN_SERVER (Options: 'backendOnly', 'webOnly', or 'bothServers') and for CREATE_SCHEMA_FOR_K8S (Options: 'true', or 'false')"
  exit 1
fi
