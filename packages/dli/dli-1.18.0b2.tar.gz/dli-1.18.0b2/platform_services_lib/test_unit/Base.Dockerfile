FROM ubuntu:21.10
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update
RUN apt-get -y install python3
RUN apt-get -y install gcc git python3-pip apt-utils unzip python-dev && \
	apt-get clean
RUN apt-get -y remove python2

RUN ln -sfn /usr/bin/python3 /usr/bin/python
