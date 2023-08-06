#!/bin/bash
set -e
set -x

ECR="116944431457.dkr.ecr.eu-west-1.amazonaws.com/platform-services-lib/base"
LATEST="test-local-platform-lib-base:latest"
LATEST_="test-local-platform-lib-base-latest"

docker tag $LATEST $ECR:$LATEST_
docker push $ECR:$LATEST_
