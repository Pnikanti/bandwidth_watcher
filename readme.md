# 🌍 Bandwidth watcher 
### "Bandwidth is measured as the amount of data that can be transferred from one point to another within a network in a specific amount of time."
## ⚙️ Configuration
Bandwidth watcher currently only supports InfluxDB - Huawei router combination.
Check out configuration file for possible configuration combinations.
## 🏴‍☠️ Bootstrapping
Bandwith Watcher uses pipenv. To install dependencies, please ensure that you have [**pipenv**](https://pypi.org/project/pipenv/) installed.

## 🗝️ Environment variables a.k.a. secrets

    DATABASE_USERNAME
    DATABASE_PASSWORD
    ROUTER_USERNAME
    ROUTER_PASSWORD

### 🛠️ Development environment 
Developing Bandwidth Watcher?

    pipenv install --pre --dev
    pipenv shell
    which python --> should output virtualenv python

## Documentation
Documentation will be done via [**mermaid**](https://github.com/mermaid-js/mermaid).