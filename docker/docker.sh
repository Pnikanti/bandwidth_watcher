#!/bin/bash
echo "Make sure you starting this script from Docker folder!"
echo "$PWD"

if [ $1 == "start" ] ; then
    echo "Starting Docker services" 
    docker-compose up --build -d
    exit 0
elif [ $1 == "stop" ] ; then
    echo "Stopping Docker services"
    docker-compose down
    exit 0
elif [ $1 == "help" ] ; then
    echo "Use docker.sh start to start container stack."
    echo "Use docker.sh stop to stop container stack."
    exit 0
else
    echo "Could not understand argument '$1'. Please refer to docker.sh help" >&2
    exit 1
fi