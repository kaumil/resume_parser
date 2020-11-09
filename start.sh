#!/bin/bash
app="docker.test"
docker build -t ${app} .
docker run -d -p 56733:80 \
  --build-arg HTTP_PROXY=http://127.0.0.1:5000
  --name=${app} \
  -v $PWD:/app ${app}
  --net=host