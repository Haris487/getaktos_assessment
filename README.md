# GETAKTOS Django Backend

> Take home assessment of GETAKTOS

### Completed Tasks

1. Created a command that populate data form csv to datastore ✓
2. API endpoint that uses request params to filter the set of consumers ✓
3. API endpoint URL is /consumers ✓
4. API responds with valid GeoJSON ✓
5. API should correctly filter any combination of API parameters ✓
6. Pagination via web linking ✓
7. Unit Tests for the endpoint ✓
8. Added rate-limiting 10 requests / second ✓
### Prerequisite

1. [Install Python 3.9.6](https://www.python.org/downloads/)
2. [Install VirtualEnv](https://virtualenv.pypa.io/en/latest/installation.html)
3. [Install Django 4.2](https://docs.djangoproject.com/en/4.2/topics/install/)
4. [Install PyCharm (Preferred IDE)](https://www.jetbrains.com/pycharm/download/)

#### Getting Started

- Clone the repo from `https://github.com/Haris487/getaktos_assessment.git`
```commandline
    git clone https://github.com/Haris487/getaktos_assessment.git
```
- Install VirtualEnv

```shell
python -m pip install --upgrade pip
pip install virtualenv
cd getaktos_assessment
virtualenv -p python3 venv
```

### Database Setup

- Install Postgres, Any other database that Django supports will also works
- Setup database

**1.**
Run this command:

```shell
su postgres
psql
```

**2.**
Run this command:

```sql
CREATE USER getaktos WITH ENCRYPTED PASSWORD 'getaktos';
```

```sql
ALTER USER getaktos CREATEDB;
```

**3**
Run these command:

```sql
CREATE DATABASE getaktos with owner getaktos;
```

### Run the Backend

In **getaktos_assessment** folder you will find requirements.txt file

#### Run this command to install the required packages:

```shell
pip install -r requirements.txt
```

### create the environment configuration

Copy the variables mentioned below in a file .envfolder/local.env

```shell
  #!/bin/bash

  export ALLOWED_HOSTS=localhost
  export DATABASE_URL=psql://getaktos:getaktos@127.0.0.1:5432/getaktos
  export TEST_DATABASE_NAME='getaktos_test'
  export DEBUG=True
  export DJANGO_LOG_LEVEL=INFO
  export DJANGO_LOG_FOLDER="logs"
```

### Create a Logs folder

```shell
mkdir logs
```

### Run this command

```shell
source .envfolder/local.env
```

### Make the migration

```shell
python manage.py makemigrations
```

Run the migration

```shell
python manage.py migrate
```

### Populate the lookup data into the database

```shell
 python manage.py populate_consumers_data 
```

### Run the backend server

```shell
python manage.py runserver
```

## Code formatting and alignment

Before commit and pushing the code, run the following script for auto formatting and alignment the code according to the standard.

## Run Test Cases

For Unit test cases run :

```shell
python manage.py test
```

For inspecting and keeping the test database add the "--keepdb"

#### but you will need to drop the test database manually for next test run

```bash
python manage.py test --keepdb
```
