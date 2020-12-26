# 🌐 Bandwidth Watcher 
Bandwidth is measured as the amount of data that can be transferred from one point to another within a network in a specific amount of time.

## 🏗️ Setup
Bandwith Watcher uses pipenv, to install dependencies, please ensure that you have [**pipenv**](https://pypi.org/project/pipenv/) installed.

## 🌲 Services
Bandwidth Watcher tries by default to save the measurements to InfluxDB. To get InfluxDB and other services, get [**Docker**](https://www.docker.com/).<br>
Start Docker services with premade script or start them by hand with docker-compose.

    bash docker/docker.sh start --> start services
    bash docker/docker.sh stop --> stop services

### 🛠️ Development environment 
Developing Bandwidth Watcher?

    pipenv install --pre --dev
    pipenv shell
    which python --> should output virtualenv python

### 🤖 Automating
Automating Bandwidth Watcher? Use premade cron script. <br>
Check [**crontab guru**](https://crontab.guru/) for scheduling!

    bash scripts/cron.sh > cron-output.log 2>&1