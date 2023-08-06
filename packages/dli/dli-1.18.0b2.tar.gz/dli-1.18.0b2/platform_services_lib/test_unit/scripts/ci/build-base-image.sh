#!/bin/bash

# debug mode
set -x

# fail script at first failed command
set -e

echo "Building $CI_PROJECT_NAME..."

# Build an image setup for testing
# Also inject the env vars used by the healthcheck endpoint.
docker build \
 -f test_unit/Base.Dockerfile \
 -t "test-local-platform-lib-base" \
 --build-arg IMAGE="base-$CI_COMMIT_SHORT_SHA" \
 .


