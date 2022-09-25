#!/usr/bin/env bash

cd $1
sudo docker build -t myimage --build-arg FILE=./index.html .
sudo docker tag myimage:latest weropanika/myimage:latest
sudo docker login
sudo docker push weropanika/myimage:latest

