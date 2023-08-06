FROM 116944431457.dkr.ecr.eu-west-1.amazonaws.com/platform-services-lib/base:test-local-platform-lib-base-latest

WORKDIR /repofiles/

COPY ./lib/ /repofiles/lib/
COPY requirements.txt /repofiles/
COPY test_unit/config/requirements-test.txt /repofiles/

RUN pip3 install -r /repofiles/requirements.txt
RUN pip3 install -r /repofiles/requirements-test.txt
