#!/bin/bash

# debug mode
set -x

# fail script at first failed command
set -e

if [[ -z $1 ]] ; then
  echo "Building $CI_PROJECT_NAME..."
  COMMIT_TAG="$ECR_REG:$CI_COMMIT_SHORT_SHA"

  # Build an image setup for testing
  # Also inject the env vars used by the healthcheck endpoint.
  docker build \
   -f test_unit/Dockerfile \
   -t "$COMMIT_TAG" \
   --build-arg IMAGE="base-$CI_COMMIT_SHORT_SHA" \
   .


  echo "Pushing images to ECR!"
  docker push "$COMMIT_TAG"
else
    # local trial build under name provided
  # n.b. make sure to set env vars (run  export $(cat ./development.local.env | xargs) && ... )
  docker build -f test_unit/Dockerfile \
  -t "$1:latest" \
   --build-arg IMAGE="base-$CI_COMMIT_SHORT_SHA" \
  .

fi
