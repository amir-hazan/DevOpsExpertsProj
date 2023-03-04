
# DevOps Experts Course - Final Project
```
Python (flask), MySQL, Docker, Jenkins and Kubernetes (HELM Chart with Flask Deployment MySql StatefulSet application) Project 
```

## Main Python Libraries

 - pymysql
 - PyPika
 - requests
 - flask
 - selenium
 - webdriver
 - prettytable
 - names
 - psutil

## Requirements Installations
```bash
pip install --ignore-installed --trusted-host pypi.python.org -r requirements.txt
```
    MySql DB configuration: Config.json (Folder: Src.Config) 

    For Creating DB tables please run create_db_tables.py (Folder: src.db) 

## Docker

- required docker & docker compose installed
```
- commands:

  - docker-compose --env-file .env --file docker_app\docker-compose.yml up --build
  - docker-compose --env-file .env --file docker_app\docker-compose.yml down --rmi all --volumes
```

## Kubernetes

- required kubectl, minikube, helm installation.
```
- commands:

  - minikube start
  - helm create namespace <namespace_name>
  - helm install devops-experts-proj-chart --namespace <namespace_name>
  - get ports (flask, mysql):
    - minikube service flask-app-svc --namespace <namespace_name>
    - minikube service mysql --namespace <namespace_name>
  - uninstall helm:
    - helm delete devops-experts-proj-chart --namespace <namespace_name>
  - delete namespace:
    - kubectl delete namespace <namespace_name>
  - stop and delete minikube server:
    - minikube stop
    - minikube delete --purge
  - delete docker image id: 
    - docker rmi <image_id>.
```

## API Reference:
### Rest Application: 
    require running rest_app.py (currently it points to: http://127.0.0.1:5000/{endpoint})
### Create user

```http  
  POST /users/${user_id}
```


| Parameter | Type  | Description           |
|:----------|:------|:----------------------|
| `user_id` | `int` | **Required**. user_id |


#### request body (json):

```json  
  {
      "user_name": "desired_username"
  }
```

### Update user name

```http  
  PUT /users/${user_id}
```


| Parameter | Type  | Description           |
|:----------|:------|:----------------------|
| `user_id` | `int` | **Required**. user_id |


#### request body (json):

```json  
  {
      "user_name": "desired_username"
  }
```

### Get user

```http
  GET /users/${user_id}
```

| Parameter | Type  | Description                           |
|:----------|:------|:--------------------------------------|
| `user_id` | `int` | **Required**. user_id of int to fetch |

#### Body response:

```json  
  {
    "status": "OK",
    "user_id": 1,
    "user_name": "desired_username"
  } 
```

### Delete user

```http
  DELETE /users/${user_id}
```

| Parameter | Type  | Description                           |
|:----------|:------|:--------------------------------------|
| `user_id` | `int` | **Required**. user_id of int to fetch |

#### Body response:

```json  
  {
    "isDeleted": true,
    "status": "OK",
    "user_id": 1
  } 
```

### Create User with auto id

```http
  POST /users/add-new-user
```

#### request body (json):

```json  
  {
      "user_name": "desired_username"
  }
```

#### Body response:

```json
  {
        "status": "OK",
        "user_id": 1,
        "user_name": "desired_username"
  }
```

### Get All users

```http
  GET users/json/get-all-users
```

#### Body response:

```json  
  [
    {
        "id": 1,
        "user_name": "desired_username",
        "date_created": "2023-01-01 01:48:44"
    },
    {
        "id": 2,
        "user_name": "desired_username",
        "date_created": "2023-01-01 01:49:08"
    }
  ]
```


### Get Config Table

```http
  GET /admin/json/get-config-table
```

#### Body response:

```json  
  [
    {
        "id": 1,
        "protocol": "http",
        "flaskHostAddress": "0.0.0.0",
        "serverTestingHostAddress": "127.0.0.1",
        "restAppPort": 5000,
        "webAppPort": 5001,
        "usersEndpoint": "users",
        "getUsersDataEndpoint": "users/get-user-data",
        "createUsersEndpoint": "users/add-new-user",
        "getAllUsersEndpoint": "users/json/get-all-users",
        "stopRestServerEndpoint": "admin/stop-rest-server",
        "stopWebServerEndpoint": "admin/stop-web-server",
        "testingBrowser": "Chrome",
        "testingUserName": "amir"
    }
  ]
```

```http
  GET /admin/stop-rest-server
```

```http
  Response:
```

```json
  {
      "status": "web server sucssfully stopped",
      "is died": "True"
  }
```


## Web Application: 
    return HTML Page with username from DB

    URL: http://127.0.0.1:5001/{endpoint}

```http
  GET /users/get-user-data/<user_id>
```

    response:

    return f"<p id='userNameErr' style='font-size: 40px'><b> No such ID</b></p>", 500

    or

    return f"<p id='userName' style='font-size: 40px'><b>Hello <span id='uName'>{user_name}</span></b></p>", 200

```http
  GET /users/get-users-table
```

    response (users table as HTML)

```http
  GET /get_config_table
```

    response (config table as HTML)

```http
  GET /admin/stop-web-server
```

```http
  Response:
```

```json
  {
      "status": "web server sucssfully stopped",
      "is died": "True"
  }
```

## Testings (Folder: src.testings):

    In Order to preform testings please run (rest_app.py & web_app.py)

    rest_app.py address: http://127.0.0.1:5000/{endpoint}

    web_app.py address: http://127.0.0.1:5001/{endpoint}

```note
Windows users: 

Please note, Chrome web driver is located in \src\web_driver folder 
and its supporting Chrome Version 109.0.5414.120 (Official Build) (64-bit) 
```
```note
Unix users:

please add chrome driver to /src/web_driver directory.
```

 - backend_testing.py
 - combined_testings.py
 - frontend_testing.py

## Authors:

- [@amir-hazan](https://www.github.com/amir-hazan)
