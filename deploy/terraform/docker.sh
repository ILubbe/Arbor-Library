#!/bin/bash

# build and push images to ecr

repo=${1}
dir=${2}
region=${3}

docker build -t ${repo}:latest ${dir} && \
aws ecr get-login-password --region ${region} | \
docker login --username AWS --password-stdin ${repo} && \
docker push ${repo}:latest