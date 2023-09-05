FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install \
    git \
    python3 \
    python3-pip \
    python3.8-venv \
    -y
# RUN python3.8-venv libgdal-dev -y
RUN pip3 install build twine
RUN pip3 install --upgrade setuptools
